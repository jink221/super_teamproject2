import json
from pathlib import Path

# 1. 정제할 JSON 파일 경로들을 모두 넣어주세요
JSON_FILES = [
    r"D:/아카이브.ver2/train_captions.json",
    r"D:/아카이브.ver2/val_captions.json",
    r"D:/아카이브.ver2/test_captions.json"  
]

def refine_captions(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_count = 0
    for item in data:
        caption = item['caption'].strip()
        
        # 첫 번째 마침표(.)를 기준으로 문장을 자름
        if '.' in caption:
            # 마침표 앞부분만 가져오고, 불필요한 공백 제거
            first_sentence = caption.split('.')[0].strip()
            
            # 문장 끝에 남은 'andymum' 같은 파편이나 너무 짧은 단어 방지 로직
            words = first_sentence.split()
            if words:
                # 마지막 단어가 1글자이거나 이상한 기호면 제거 (선택 사항)
                if len(words[-1]) < 2 and not words[-1].isalnum():
                    words.pop()
                
                new_caption = " ".join(words) + "."
                
                # 원본과 다를 경우에만 교체 및 카운트
                if new_caption != caption:
                    item['caption'] = new_caption
                    cleaned_count += 1
        else:
            # 마침표가 아예 없는 문장도 마침표를 찍어줌 (안전장치)
            item['caption'] = caption + "."

    # 'refined_' 접두사를 붙여서 새 파일로 저장 (원본 보존)
    save_path = path.parent / f"refined_{path.name}"
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ {path.name} 정제 완료! (수정됨: {cleaned_count}개)")

# 실행
for file in JSON_FILES:
    refine_captions(file)

print("\n✨ 모든 파일 정제가 끝났습니다. 이제 'refined_'가 붙은 파일들을 최종본으로 사용하세요!")