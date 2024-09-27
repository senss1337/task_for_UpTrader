import os
import sys
from dotenv import load_dotenv
from pathlib import Path

if __name__ == '__main__':
    env_path = Path(__file__).resolve().parent / '.env'
    load_dotenv(dotenv_path=env_path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django..."
        ) from exc
    execute_from_command_line(sys.argv)
