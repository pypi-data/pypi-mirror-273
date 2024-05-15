from elemental_tools.test import Test, NewTest
from elemental_tools.system import generate_reference


class GenerateReferenceTest(Test):
    _test_pyobject_id = generate_reference()

    load = [
        NewTest(
            name='elemental_tools.db.generator.generate_reference',
            function=generate_reference,
            args=(_test_pyobject_id,),
            expected_result=_test_pyobject_id
        ),
    ]


test_pyobject_id = GenerateReferenceTest(supress_log=True, repeat_load=100)
test_pyobject_id.run()
test_pyobject_id.result()
