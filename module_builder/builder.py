import os
import json
from datetime import datetime
from argparse import ArgumentParser
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'db.sqlite3'))
engine = create_engine(f'sqlite:///{DB_PATH}')


def get_module_data(module_name):
    module_path = os.path.join(BASE_DIR, '..', 'modules', module_name)
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module {module_name} not found")
    try:
        with open(os.path.join(module_path, 'config.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"config.json file not found for module {module_name}")


def organize_module_data(data):
    name = data.get("name")
    description = data.get("description", "")
    premium = data.get("premium", False)
    type_ = data.get("type", "default")
    inputs = data.get("inputs", "")
    outputs = data.get("outputs", "")
    repository = data.get("repository", "")
    backend = name
    is_active = data.get("is_active", True)
    max_results = data.get("max_results", 10)
    return name, description, premium, type_, inputs, outputs, repository, backend, is_active, max_results


def build_module(module_name):
    config = get_module_data(module_name)
    name, description, premium, type_, inputs, outputs, repository, backend, is_active, max_results = organize_module_data(config)

    created_at = datetime.now()
    updated_at = datetime.now()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM modules_api_module WHERE name = :name"),
            {"name": name}
        ).fetchone()

        params = {
            "name": name,
            "description": description,
            "premium": premium,
            "type": type_,
            "inputs": json.dumps(inputs),
            "outputs": json.dumps(outputs),
            "repository": repository,
            "backend": backend,
            "is_active": is_active,
            "created_at": created_at,
            "updated_at": updated_at,
            "max_results": max_results,
        }

        if not result:
            conn.execute(
                text("""
                    INSERT INTO modules_api_module 
                    (name, description, premium, type, inputs, outputs, repository, backend, is_active, created_at, updated_at, max_results)
                    VALUES (:name, :description, :premium, :type, :inputs, :outputs, :repository, :backend, :is_active, :created_at, :updated_at, :max_results)
                """),
                params
            )
        else:
            conn.execute(
                text("""
                    UPDATE modules_api_module 
                    SET description = :description, premium = :premium, type = :type,
                        inputs = :inputs, outputs = :outputs, repository = :repository, backend = :backend,
                        is_active = :is_active, updated_at = :updated_at, max_results = :max_results
                    WHERE name = :name
                """),
                params
            )
        conn.commit()
        print(f"Module '{name}' built successfully.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", type=str, required=True, help="The name of the module to build on frontend")
    args = parser.parse_args()
    build_module(args.m)
