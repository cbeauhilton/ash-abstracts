import os

from deta import Deta

project_id = os.environ.get("DETA_ID_ASH")
API_key = os.environ.get("DETA_TOKEN_ASH")
deta = Deta(API_key)

drive = deta.Drive("base")
done = drive.put(path="../data/base.db", name="base.db")
print(f"{done} saved to {project_id}.")

## test that it worked by downloading it to a different filename
# large_file = drive.get("base.db")
# with open("large_file.db", "wb+") as f:
#     for chunk in large_file.iter_chunks(4096):
#         f.write(chunk)
#     large_file.close()
