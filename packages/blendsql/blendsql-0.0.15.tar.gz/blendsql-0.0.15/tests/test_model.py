import uuid
from dataclasses import dataclass
from blendsql.models import Model
from blendsql._program import Program

TEST_QUESTION = "The quick brown fox jumps over the lazy dog"

MODEL_A = "a"
MODEL_B = "b"


@dataclass
class DummyModelOutput:
    _variables: dict


class DummyModel(Model):
    def __init__(self, model_name_or_path: str, **kwargs):
        super().__init__(
            model_name_or_path=model_name_or_path,
            requires_config=False,
            tokenizer=None,
            **kwargs,
        )

    def _load_model(self):
        return self.model_name_or_path


class DummyProgram(Program):
    def __new__(
        self,
        **kwargs,
    ):
        return self.__call__(self, **kwargs)

    def __call__(self, question: str, **kwargs):
        return DummyModelOutput({"uuid": str(uuid.uuid4())})


class DifferentDummyProgram(Program):
    def __new__(
        self,
        **kwargs,
    ):
        return self.__call__(self, **kwargs)

    def __call__(self, question: str, unused: str = None, **kwargs):
        return DummyModelOutput({"uuid": str(uuid.uuid4())})


class DummyProgramWithGlobal(Program):
    def __new__(
        self,
        **kwargs,
    ):
        return self.__call__(self, **kwargs)

    def __call__(self, question: str, **kwargs):
        print(TEST_GLOBAL)
        return DummyModelOutput({"uuid": str(uuid.uuid4())})


def test_simple_cache():
    a = DummyModel(MODEL_A).predict(program=DummyProgram, question=TEST_QUESTION)[
        "uuid"
    ]

    model_b = DummyModel(MODEL_A)
    b = model_b.predict(program=DummyProgram, question=TEST_QUESTION)["uuid"]

    assert a == b
    assert model_b.num_llm_calls == 0


def test_different_models():
    a = DummyModel(MODEL_A).predict(program=DummyProgram, question=TEST_QUESTION)[
        "uuid"
    ]

    b = DummyModel(MODEL_B).predict(program=DummyProgram, question=TEST_QUESTION)[
        "uuid"
    ]

    assert a != b


def test_different_arguments():
    a = DummyModel(MODEL_A).predict(program=DummyProgram, question=TEST_QUESTION)[
        "uuid"
    ]

    b = DummyModel(MODEL_A).predict(
        program=DummyProgram, question="This is a different question"
    )["uuid"]

    assert a != b


def test_different_programs():
    a = DummyModel(MODEL_A).predict(program=DummyProgram, question=TEST_QUESTION)[
        "uuid"
    ]

    b = DummyModel(MODEL_A).predict(
        program=DifferentDummyProgram, question=TEST_QUESTION
    )["uuid"]

    assert a != b


def test_same_global_vars():
    global TEST_GLOBAL
    TEST_GLOBAL = "This is the same value"
    a = DummyModel(MODEL_A).predict(
        program=DummyProgramWithGlobal, question=TEST_QUESTION
    )["uuid"]

    TEST_GLOBAL = "This is the same value"
    model_b = DummyModel(MODEL_A)
    b = model_b.predict(program=DummyProgramWithGlobal, question=TEST_QUESTION)["uuid"]

    assert a == b
    assert model_b.num_llm_calls == 0


def test_different_global_vars():
    global TEST_GLOBAL
    TEST_GLOBAL = "This is one value"
    a = DummyModel(MODEL_A).predict(
        program=DummyProgramWithGlobal, question=TEST_QUESTION
    )["uuid"]

    TEST_GLOBAL = "This is a different value"
    b = DummyModel(MODEL_A).predict(
        program=DummyProgramWithGlobal, question=TEST_QUESTION
    )["uuid"]

    assert a != b


def test_with_set_vars():
    a = DummyModel(MODEL_A).predict(
        program=DummyProgram, question=TEST_QUESTION, random_set={"a", "b", "c"}
    )["uuid"]

    b = DummyModel(MODEL_A).predict(
        program=DummyProgram, question=TEST_QUESTION, random_set={"b", "c", "a"}
    )["uuid"]

    assert a == b
