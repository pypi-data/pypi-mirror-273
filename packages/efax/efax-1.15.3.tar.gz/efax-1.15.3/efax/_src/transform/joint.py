from collections.abc import Mapping
from functools import reduce
from typing import Any, override

import jax.numpy as jnp
from tjax import JaxRealArray, Shape
from tjax.dataclasses import dataclass, field

from ..expectation_parametrization import ExpectationParametrization
from ..natural_parametrization import NaturalParametrization
from ..parametrization import Parametrization


@dataclass
class JointDistribution(Parametrization):
    sub_distributions_objects: Mapping[str, Parametrization] = field(
            static=False, metadata={'subdistribution': True, 'parameter': False})
    sub_distributions_classes: Mapping[str, type[NaturalParametrization[Any, Any]]] = field(
            static=True, metadata={'subdistribution': True, 'parameter': False}, init=False)

    def __post_init__(self) -> None:
        def g(t: type[Parametrization]) -> type[NaturalParametrization[Any, Any]]:
            if issubclass(t, NaturalParametrization):
                return t
            assert issubclass(t, ExpectationParametrization)
            return t.natural_parametrization_cls()
        sub_distributions_classes = {name: g(type(value))
                                     for name, value in self.sub_distributions_objects.items()}
        object.__setattr__(self, 'sub_distributions_classes', sub_distributions_classes)

    @property
    @override
    def shape(self) -> Shape:
        first = next(iter(self.sub_distributions_objects.values()))
        return first.shape

    @override
    def sub_distributions(self) -> Mapping[str, Parametrization]:
        return self.sub_distributions_objects


@dataclass
class JointDistributionE(JointDistribution,
                         ExpectationParametrization['JointDistributionN']):
    sub_distributions_objects: Mapping[str, ExpectationParametrization[Any]] = field(
            static=False, metadata={'subdistribution': True, 'parameter': False})

    @override
    def sub_distributions(self) -> Mapping[str, ExpectationParametrization[Any]]:
        return self.sub_distributions_objects

    @classmethod
    @override
    def natural_parametrization_cls(cls) -> type['JointDistributionN']:
        return JointDistributionN

    @override
    def to_nat(self) -> 'JointDistributionN':
        return JointDistributionN({name: value.to_nat()
                                   for name, value in self.sub_distributions_objects.items()})


@dataclass
class JointDistributionN(JointDistribution,
                         NaturalParametrization[JointDistributionE, dict[str, Any]]):
    sub_distributions_objects: Mapping[str, NaturalParametrization[Any, Any]] = field(
            static=False, metadata={'subdistribution': True, 'parameter': False})

    @override
    def sub_distributions(self) -> Mapping[str, NaturalParametrization[Any, Any]]:
        return self.sub_distributions_objects

    @override
    def log_normalizer(self) -> JaxRealArray:
        return reduce(jnp.add,
                      (x.log_normalizer() for x in self.sub_distributions_objects.values()))

    @override
    def to_exp(self) -> JointDistributionE:
        return JointDistributionE({name: value.to_exp()
                                   for name, value in self.sub_distributions_objects.items()})

    @override
    def carrier_measure(self, x: dict[str, Any]) -> JaxRealArray:
        return reduce(jnp.add,
                      (value.carrier_measure(x[name])
                       for name, value in self.sub_distributions_objects.items()))

    @classmethod
    @override
    def sufficient_statistics(cls, x: dict[str, Any], **fixed_parameters: Any
                              ) -> JointDistributionE:
        sub_distributions_classes = fixed_parameters.pop('sub_distributions_classes')
        return JointDistributionE(
            {name: value.sufficient_statistics(x[name], **fixed_parameters.get(name, {}))
             for name, value in sub_distributions_classes.items()})
# @dataclass
# class RivalMessagePrediction:
#     """A distribution over a RivalMessage."""
#     attention: GammaNP
#     rivals: NormalNP
#
#     @classmethod
#     def zeros(cls, attention_features: int, rivals_features: int) -> Self:
#         za = jnp.zeros(attention_features)
#         zr = jnp.zeros(rivals_features)
#         attention = GammaNP(za, za)
#         rivals = NormalNP(zr, zr)
#         return cls(attention, rivals)
#
#     def sample(self, key: KeyArray, shape: Shape | None = None) -> RivalMessage:
#         attention_key, rivals_key = split(key)
#         # TODO: Sample the gamma distribution when the Hessian of the variates is supported.
#         # attention = self.attention.sample(attention_key, shape)
#         gamma_vp = self.attention.to_var()
#         exponential = ExponentialEP(gamma_vp.mean)
#         attention = exponential.sample(attention_key)
#         rivals = self.rivals.to_exp().sample(rivals_key, shape)
#         return RivalMessage(attention, rivals)
#
#     def mean(self) -> RivalMessage:
#         attention = self.attention.to_exp().mean
#         rivals = self.rivals.to_exp().mean
#         return RivalMessage(attention, rivals)
#
#     def log_pdf(self, message: RivalMessage) -> RivalMessageEnergy:
#         return RivalMessageEnergy(jnp.sum(self.attention.log_pdf(message.attention), axis=-1),
#                                   jnp.sum(self.rivals.log_pdf(message.rivals), axis=-1))
#
#     def kl_divergence(self, predictor: RivalMessagePrediction) -> RivalMessageEnergy:
#         return RivalMessageEnergy(jnp.sum(self.attention.kl_divergence(predictor.attention),
#                                           axis=-1),
#                                   jnp.sum(self.rivals.kl_divergence(predictor.rivals), axis=-1))
