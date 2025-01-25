import argparse
from golynx.config import Config, DatabaseType
from golynx.infrastructure.database.provider import DatabaseProvider
from golynx.infrastructure.storage.disk import Disk

def main():
    parser = argparse.ArgumentParser(description='This script migrates data from one datasource to another')
    parser.add_argument('--from', dest='from_path', type=str, choices=[t.value for t in DatabaseType],
                      required=True, help='Source database type to migrate from')
    parser.add_argument('--to', dest='to_path', type=str, choices=[t.value for t in DatabaseType],
                      required=True, help='Destination database type to migrate to')

    args = parser.parse_args()
    storage: Disk = Disk(
        flush_dir=Config.STORAGE_FLUSH_DIR,
        flush_file=Config.STORAGE_FLUSH_FILE,
    )
    from_db_type = DatabaseType(args.from_path)
    to_db_type = DatabaseType(args.to_path)
    
    from_provider = DatabaseProvider(from_db_type).get()()
    from_provider.initialize(storage=storage)
    to_provider = DatabaseProvider(to_db_type).get()()
    to_provider.initialize(storage=storage)
    
    print(f"Migrating from {from_db_type.value} to {to_db_type.value}")
    print(f"Total {from_db_type.value} links: {len(from_provider.get_all())}")
    print(f"Total {to_db_type.value} links: {len(to_provider.get_all())}")
    
    to_provider.truncate()
    for golink in from_provider.get_all(as_dict=False).values():
      print("Inserting", golink)
      try:
        to_provider.set(golink)
      except Exception as e:
        print(f"Error inserting {golink.link}: {e}")
    
    to_provider.flush()
    
    
if __name__ == '__main__':
    main()