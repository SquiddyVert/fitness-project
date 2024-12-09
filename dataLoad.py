import pandas as pd

df = pd.read_parquet("hf://datasets/onurSakar/GYM-Exercise/data/train-00000-of-00001.parquet")

def extract_qna(row):
    text = row["text"]
    if "[INST]" in text and "[/INST]" in text:
        question = text.split("[INST]")[1].split("[/INST]")[0].strip()
        question = question.split("<<SYS>>")[-1].split("<</SYS>>")[-1].strip()
        answer = text.split("[/INST]")[1].split("</s>")[0].strip()
        return {"question": question, "answer": answer}
    return {"question": None, "answer": None}

# Apply function to the dataframe
qna_list = df.apply(extract_qna, axis=1).tolist()
