def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # קריאת הקובץ בבלוקים כדי לא להעמיס על הזיכרון עם קבצים גדולים
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# שימוש בפונקציה
file_id = calculate_file_hash("your_podcast_file.wav")
print(f"The Unique ID is: {file_id}")