import grpc
import puan_db_pb2
import puan_db_pb2_grpc

from dataclasses import dataclass, field
from itertools import starmap
from typing import Optional, List, Dict

from puan_db_pb2 import Solver

@dataclass
class Composite:
    id: str
    references: List[str]
    bias: int
    negated: bool
    alias: List[str] = field(default_factory=list)

@dataclass
class Model:

    host: str
    port: int

    _token: str
    _parent: Optional["Model"] = None

    @staticmethod
    def _bound_complex(bound: Optional[puan_db_pb2.Bound]) -> Optional[complex]:
        return complex(bound.lower, bound.upper) if bound else None

    @staticmethod
    def _complex_bound(cmplx: complex) -> puan_db_pb2.Bound:
        return puan_db_pb2.Bound(
            lower=int(cmplx.real),
            upper=int(cmplx.imag),
        )

    @staticmethod
    def _dict_interpretation(d: Dict[str, complex]) -> puan_db_pb2.Interpretation:
        return puan_db_pb2.Interpretation(
            variables=list(
                starmap(
                    lambda k,v: puan_db_pb2.Variable(
                        id=k,
                        bound=Model._complex_bound(v),
                    ),
                    d.items()
                )
            )
        )

    @staticmethod
    def _interpretation_dict(interpretation: puan_db_pb2.Interpretation) -> Dict[str, complex]:
        return dict(
            map(
                lambda x: (x.id, Model._bound_complex(x.bound)),
                interpretation.variables
            )
        )

    @staticmethod
    def _dict_objective(d: Dict[str, int]) -> puan_db_pb2.Objective:
        return puan_db_pb2.Objective(
            variables=list(
                starmap(
                    lambda k,v: puan_db_pb2.FixedVariable(
                        id=k,
                        value=v,
                    ),
                    d.items()
                )
            )
        )

    @staticmethod
    def _objective_dict(objective: puan_db_pb2.Objective) -> Dict[str, int]:
        return dict(
            map(
                lambda x: (x.id, x.value),
                objective.variables
            )
        )
    
    @property
    def parent(self) -> Optional["Model"]:
        """
            Get the parent model of the current model.
        """
        return self._parent

    @property
    def primitives(self) -> List[str]:
        """
            Get all primitive variable id's from the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.GetPrimitiveIds(puan_db_pb2.Empty(), metadata=(("token", self._token),)).ids
        
    @property
    def composites(self) -> List[str]:
        """
            Get all composite variable id's from the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.GetCompositeIds(puan_db_pb2.Empty(), metadata=(("token", self._token),)).ids
        
    def get(self, id: str) -> complex:
        """
            Get the bound of a variable from its id.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model._bound_complex(stub.Get(puan_db_pb2.IDRequest(id=id), metadata=(("token", self._token),)))
        
    def get_composites(self) -> List[Composite]:
        """
            Get the ids of the variables in a composite variable.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return list(
                map(
                    lambda args: Composite(
                        id=args.id,
                        references=args.references,
                        bias=args.bias,
                        negated=args.negated,
                        alias=args.alias
                    ), 
                    stub.GetComposites(puan_db_pb2.Empty(), metadata=(("token", self._token),)).composites
                )
            )
        
    def id_from_alias(self, alias: str) -> Optional[str]:
        """
            Get the id of a variable from its alias.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.GetIDFromAlias(puan_db_pb2.AliasRequest(alias=alias), metadata=(("token", self._token),)).id
        
    def delete(self, id: str) -> bool:
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.Delete(puan_db_pb2.IDRequest(id=id), metadata=(("token", self._token),)).success

    def set_primitive(self, id: str, bound: complex = complex(0,1)) -> str:
        """
            Set a primitive variable in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetPrimitive(
                puan_db_pb2.Primitive(
                    id=id,
                    bound=puan_db_pb2.Bound(
                        lower=int(bound.real),
                        upper=int(bound.imag),
                    )
                ), metadata=(("token", self._token),)
            ).id
        
    def set_primitives(self, ids: List[str], bound: complex = complex(0,1)) -> List[str]:
        """
            Set multiple primitive variables with the same bound in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetPrimitives(
                puan_db_pb2.SetPrimitivesRequest(
                    ids=ids,
                    bound=puan_db_pb2.Bound(
                        lower=int(bound.real),
                        upper=int(bound.imag),
                    )
                ), metadata=(("token", self._token),)
            ).ids
        
    def set_atleast(self, references: List[str], value: int, alias: Optional[str] = None) -> str:
        """
            Set an atleast constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetAtLeast(
                puan_db_pb2.AtLeast(
                    references=references,
                    value=value,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_atmost(self, references: List[str], value: int, alias: Optional[str] = None) -> str:
        """
            Set an atmost constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetAtMost(
                puan_db_pb2.AtMost(
                    references=references,
                    value=value,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_and(self, references: List[str], alias: Optional[str] = None) -> str:
        """
            Set an and constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetAnd(
                puan_db_pb2.And(
                    references=references,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_or(self, references: List[str], alias: Optional[str] = None) -> str:
        """
            Set an or constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetOr(
                puan_db_pb2.Or(
                    references=references,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_not(self, references: List[str], alias: Optional[str] = None) -> str:
        """
            Set a not constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetNot(
                puan_db_pb2.Not(
                    references=references,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_xor(self, references: List[str], alias: Optional[str] = None) -> str:
        """
            Set an xor constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetXor(
                puan_db_pb2.Xor(
                    references=references,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_imply(self, condition: str, consequence: str, alias: Optional[str] = None) -> str:
        """
            Set an imply constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetImply(
                puan_db_pb2.Imply(
                    condition=condition,
                    consequence=consequence,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def set_equal(self, lhs: str, rhs: str, alias: Optional[str] = None) -> str:
        """
            Set an equivalent constraint in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return stub.SetEqual(
                puan_db_pb2.Equivalent(
                    lhs=lhs,
                    rhs=rhs,
                    alias=alias
                ), metadata=(("token", self._token),)
            ).id
        
    def propagate(self, query: Dict[str, complex] = {}) -> Dict[str, complex]:
        """
            Propagate constraints downstream and returns the resulted bounds.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model._interpretation_dict(
                stub.Propagate(
                    Model._dict_interpretation(query), metadata=(("token", self._token),)
                )
            )
        
    def propagate_upstream(self, query: Dict[str, complex] = {}) -> Dict[str, complex]:
        """
            Propagate constraints downstream and returns the resulted bounds.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model._interpretation_dict(
                stub.PropagateUpstream(
                    Model._dict_interpretation(query), metadata=(("token", self._token),)
                )
            )
        
    def propagate_bistream(self, query: Dict[str, complex] = {}) -> Dict[str, complex]:
        """
            Propagate constraints downstream and returns the resulted bounds.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model._interpretation_dict(
                stub.PropagateBidirectional(
                    Model._dict_interpretation(query), metadata=(("token", self._token),)
                )
            )
        
    def solve(self, objectives: List[Dict[str, int]], assume: Dict[str, int], solver: Solver) -> List[Dict[str, int]]:
        """
            Solves the objectives in the database and returns the optimal values.

            objectives:     List of objective dictionaries.
            fix:            Variables to be fixed before the optimization.
            solver:         Solver to be used.

            Returns:        List of optimal values.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return list(
                map(
                    Model._interpretation_dict,
                    stub.Solve(
                        puan_db_pb2.SolveRequest(
                            objectives=list(map(Model._dict_objective, objectives)),
                            assume=Model._dict_interpretation(assume),
                            solver=solver
                        ), metadata=(("token", self._token),)
                    ).solutions
                )
            )
        
    def cut(self, cuts: Dict[str, str]) -> "Model":
        """
            Cut the given nodes. The sub tree under the given nodes will be removed.
            Each cut node will be replaced with a new primitive variable, which ID is the `value` in `cuts`.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model(
                host=self.host, 
                port=self.port, 
                _token=stub.Cut(
                    puan_db_pb2.CutRequest(
                        cuts=list(
                            starmap(
                                lambda k,v: puan_db_pb2.CutVariableMapping(
                                    from_id=k,
                                    to_id=v,
                                ),
                                cuts.items()
                            )
                        ),
                    ), metadata=(("token", self._token),)
                ).token,
                _parent=self,
            )
        
    def sub(self, roots: List[str]) -> "Model":
        """
            Create a submodel from the given roots.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model(
                host=self.host, 
                port=self.port, 
                _token=stub.Sub(puan_db_pb2.SubRequest(ids=roots), metadata=(("token", self._token),)).token,
                _parent=self,
            )
        
    def cut_sub(self, cuts: Dict[str, str], roots: List[str]) -> "Model":
        """
            Cuts the given nodes and creates a submodel from the given roots.
            Each cut node will be replaced with a new primitive variable, which ID is the `value` in `cuts`.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            return Model(
                host=self.host, 
                port=self.port, 
                _token=stub.CutSub(
                    puan_db_pb2.CutSubRequest(
                        cut=puan_db_pb2.CutRequest(
                            cut_ids=list(
                                starmap(
                                    lambda k,v: puan_db_pb2.CutVariableMapping(
                                        from_id=k,
                                        to_id=v,
                                    ),
                                    cuts.items()
                                )
                            )
                        ), 
                        sub=puan_db_pb2.SubRequest(ids=roots),
                    ), metadata=(("token", self._token),)
                ).token,
                _parent=self,
            )

@dataclass
class PuanClient:

    host:       str
    port:       int
    password:   Optional[str] = None
    ssl:        Optional[bool] = None

    def select(self, id: str, password: str) -> Model:
        """
            Select a model from the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            result = stub.ModelSelect(
                puan_db_pb2.SelectModelRequest(
                    id=id,
                    password=password,
                )
            )
            if not result.success:
                raise Exception("Model not found.")
            return Model(host=self.host, port=self.port, _token=result.token)
        
    def create(self, id: str, password: str) -> Model:
        """
            Create a model in the database.
        """
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = puan_db_pb2_grpc.ModelingServiceStub(channel)
            result = stub.ModelCreate(
                puan_db_pb2.CreateModelRequest(
                    id=id,
                    password=password,
                )
            )
            if not result.success:
                raise Exception("Could not create model.")
            return Model(host=self.host, port=self.port, _token=result.token)