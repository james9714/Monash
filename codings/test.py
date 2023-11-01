file_path = "演示文稿.txt"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()
print("原文本：", text)
print("-"*50)
text = text.strip("。").split("。")
for i in range(len(text)):
    print("第{}句话：{}".format(i+1, text[i]))