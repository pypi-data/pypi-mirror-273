from elemental_tools.asserts import root_ref, config
from elemental_tools.pydantic import generate_script_information_from_pydantic_models, generate_pydantic_model_from_path
from elemental_tools.scripts.google_synchronization import main as g_sync

scripts_information = generate_pydantic_model_from_path(config.scripts_root_path)
print(scripts_information)
#def test_google_sync():
#    g_sync.start(root_ref)

