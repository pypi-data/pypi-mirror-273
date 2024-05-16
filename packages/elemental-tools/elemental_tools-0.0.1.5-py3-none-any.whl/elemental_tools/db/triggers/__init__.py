from sqlalchemy import text


def trigger_validate_ref_in_table(ref_alias, table_to_trigger, validation_table, ref_alias_on_validation_table: str = "ref"):
    trigger_name = f"trigger_{ref_alias}_in_{validation_table}"
    function_name = f"fn_check_{ref_alias}_in_{validation_table}"

    trigger_sql = f"""
    CREATE OR REPLACE FUNCTION {function_name}()
    RETURNS TRIGGER AS
    $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM {validation_table} WHERE {ref_alias_on_validation_table} = NEW.{ref_alias}
        ) THEN
            RAISE EXCEPTION '{ref_alias} not found in {validation_table}';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER {trigger_name}
    BEFORE INSERT OR UPDATE ON {table_to_trigger}
    FOR EACH ROW
    EXECUTE FUNCTION {function_name}();
    """
    return text(trigger_sql)

