from src.chroma_utils import vectorstore

# INPUT FILE ID
file_id = "6a1882c57ce6eb524ffff595"   # replace with your actual file_id

# Fetch only this file's chunks
docs = vectorstore.get(
    where={"file_id": file_id},
    include=["documents", "metadatas", "embeddings"]
)

print("===================================")
print("FILE ID:", file_id)
print("TOTAL CHUNKS:", len(docs["ids"]))

for i in range(len(docs["ids"])):
    print(f"\n------ Chunk {i+1} ------")

    print("Chunk ID:", docs["ids"][i])

    print("Metadata:")
    print(docs["metadatas"][i])

    print("Embedding Length:")
    print(len(docs["embeddings"][i]))

    print("Embedding Preview:")
    print(docs["embeddings"][i][:10])   # first 10 values

    print("Text Preview:")
    print(docs["documents"][i][:300])