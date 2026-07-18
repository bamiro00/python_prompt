import json
from pathlib import Path


DATA_FILE = Path("prompts.json")
EXPORT_DIR = Path("exports")

# 프롬프트에서 사용할 카테고리 목록
CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]


# 프로그램을 시작할 때 기본으로 등록되는 프롬프트
prompts = [
    {
        "id": 1,
        "title": "반려동물 성장일기 작성",
        "content": (
            "반려동물의 이름, 나이, 성격, 오늘 있었던 일을 바탕으로 "
            "따뜻하고 자연스러운 성장일기를 작성해 주세요."
        ),
        "category": "텍스트 생성",
        "favorite": False,
    },
    {
        "id": 2,
        "title": "반려동물 추억 일러스트 기획",
        "content": (
            "반려동물의 외모와 기억에 남는 순간을 바탕으로 "
            "따뜻한 동화책 스타일의 추억 일러스트를 기획해 주세요."
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "id": 3,
        "title": "반려동물 추억 영상 스토리보드",
        "content": (
            "반려동물의 어린 시절부터 현재까지의 사진을 활용하여 "
            "1분 분량의 추억 영상 스토리보드와 장면별 자막을 작성해 주세요."
        ),
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "id": 4,
        "title": "반려동물 추억 작가",
        "content": (
            "당신은 반려동물과 가족의 추억을 따뜻한 이야기로 만드는 작가입니다. "
            "사용자에게 필요한 정보를 질문한 뒤 감성적인 이야기를 작성해 주세요."
        ),
        "category": "페르소나",
        "favorite": False,
    },
    {
        "id": 5,
        "title": "반려동물 사진 정리 계획",
        "content": (
            "촬영 날짜와 상황별로 흩어진 반려동물 사진을 정리할 수 있도록 "
            "폴더 분류 기준과 주간 정리 순서를 작성해 주세요."
        ),
        "category": "자동화",
        "favorite": False,
    },
]

def save_prompts(prompt_list):
    """프롬프트 데이터를 JSON 파일로 저장한다."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                prompt_list,
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"데이터 저장 중 오류가 발생했습니다: {error}")


def load_prompts(prompt_list):
    """JSON 파일이 있으면 저장된 프롬프트를 불러온다."""
    if not DATA_FILE.exists():
        for prompt in prompt_list:
            prompt.setdefault("views", 0)

        save_prompts(prompt_list)
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            saved_prompts = json.load(file)

        if not isinstance(saved_prompts, list):
            print("저장 파일 형식이 올바르지 않아 기본 데이터로 시작합니다.")
            return

        prompt_list.clear()
        prompt_list.extend(saved_prompts)
        for prompt in prompt_list:
            prompt.setdefault("views", 0)

        save_prompts(prompt_list)

    except (OSError, json.JSONDecodeError) as error:
        print(f"데이터 불러오기 중 오류가 발생했습니다: {error}")
        print("기본 데이터로 시작합니다.")

def get_required_input(label):
    """빈값이 아닌 입력을 받을 때까지 반복한다."""
    while True:
        value = input(f"{label}: ").strip()

        if value:
            return value

        print("입력값을 비워둘 수 없습니다. 다시 입력해 주세요.")


def select_category(categories):
    """카테고리 목록을 출력하고 선택한 카테고리를 반환한다."""
    print("\n카테고리 선택")

    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("카테고리 번호: ").strip()

        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(categories):
                return categories[index]

        print("올바른 카테고리 번호를 입력해 주세요.")


def get_next_id(prompt_list):
    """새 프롬프트에 사용할 다음 번호를 반환한다."""
    if not prompt_list:
        return 1

    return max(prompt["id"] for prompt in prompt_list) + 1


def add_prompt(prompt_list, categories):
    """새로운 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")

    title = get_required_input("제목")
    content = get_required_input("내용")
    category = select_category(categories)

    new_prompt = {
        "id": get_next_id(prompt_list),
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    }

    prompt_list.append(new_prompt)
    save_prompts(prompt_list)

    print("\n프롬프트가 추가되었습니다.")
    print(f"등록 번호: {new_prompt['id']}")

def show_list(prompt_list):
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")

    if not prompt_list:
        print("등록된 프롬프트가 없습니다.")
        return

    for prompt in prompt_list:
        favorite_mark = " ⭐" if prompt["favorite"] else ""

        print(
            f"{prompt['id']}. "
            f"[{prompt['category']}] "
            f"{prompt['title']}{favorite_mark}"
        )

    print(f"\n총 {len(prompt_list)}개의 프롬프트")


def show_by_category(prompt_list, categories):
    """선택한 카테고리에 속한 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")

    selected_category = select_category(categories)

    filtered_prompts = [
        prompt
        for prompt in prompt_list
        if prompt["category"] == selected_category
    ]

    print(f"\n[{selected_category}] 카테고리 프롬프트")

    if not filtered_prompts:
        print("해당 카테고리에 등록된 프롬프트가 없습니다.")
        return

    for prompt in filtered_prompts:
        favorite_mark = " ⭐" if prompt["favorite"] else ""

        print(
            f"{prompt['id']}. "
            f"{prompt['title']}{favorite_mark}"
        )

    print(f"\n총 {len(filtered_prompts)}개의 프롬프트")


def search_prompt(prompt_list):
    """제목 또는 내용에 검색어가 포함된 프롬프트를 출력한다."""
    print("\n=== 프롬프트 검색 ===")

    keyword = get_required_input("검색어").lower()

    search_results = [
        prompt
        for prompt in prompt_list
        if keyword in prompt["title"].lower()
        or keyword in prompt["content"].lower()
    ]

    if not search_results:
        print("검색 결과가 없습니다.")
        return

    print(f"\n검색 결과: {len(search_results)}개")

    for prompt in search_results:
        favorite_mark = " ⭐" if prompt["favorite"] else ""

        print(
            f"{prompt['id']}. "
            f"[{prompt['category']}] "
            f"{prompt['title']}{favorite_mark}"
        )

def find_prompt_by_id(prompt_list, prompt_id):
    """입력한 번호와 일치하는 프롬프트를 반환한다."""
    for prompt in prompt_list:
        if prompt["id"] == prompt_id:
            return prompt

    return None


def show_detail(prompt_list):
    """선택한 프롬프트의 전체 정보를 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")

    prompt_id_text = get_required_input("프롬프트 번호")

    if not prompt_id_text.isdigit():
        print("프롬프트 번호는 숫자로 입력해 주세요.")
        return

    prompt_id = int(prompt_id_text)
    selected_prompt = find_prompt_by_id(prompt_list, prompt_id)

    if selected_prompt is None:
        print("해당 번호의 프롬프트가 없습니다.")
        return
    
    selected_prompt["views"] = selected_prompt.get("views", 0) + 1
    save_prompts(prompt_list)

    favorite_text = "예 ⭐" if selected_prompt["favorite"] else "아니오"

    print("\n" + "-" * 40)
    print(f"번호: {selected_prompt['id']}")
    print(f"제목: {selected_prompt['title']}")
    print(f"카테고리: {selected_prompt['category']}")
    print(f"즐겨찾기: {favorite_text}")
    print(f"조회수: {selected_prompt['views']}회")
    print("내용:")
    print(selected_prompt["content"])
    print("-" * 40)

def toggle_favorite(prompt_list):
    """선택한 프롬프트의 즐겨찾기 상태를 추가하거나 해제한다."""
    print("\n=== 즐겨찾기 관리 ===")

    prompt_id_text = get_required_input("프롬프트 번호")

    if not prompt_id_text.isdigit():
        print("프롬프트 번호는 숫자로 입력해 주세요.")
        return

    prompt_id = int(prompt_id_text)
    selected_prompt = find_prompt_by_id(prompt_list, prompt_id)

    if selected_prompt is None:
        print("해당 번호의 프롬프트가 없습니다.")
        return

    selected_prompt["favorite"] = not selected_prompt["favorite"]
    save_prompts(prompt_list)

    if selected_prompt["favorite"]:
        print(f"'{selected_prompt['title']}'을 즐겨찾기에 추가했습니다.")
    else:
        print(f"'{selected_prompt['title']}'을 즐겨찾기에서 해제했습니다.")

def show_favorites(prompt_list):
    """즐겨찾기로 설정된 프롬프트만 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")

    favorite_prompts = [
        prompt
        for prompt in prompt_list
        if prompt["favorite"]
    ]

    if not favorite_prompts:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    for prompt in favorite_prompts:
        print(
            f"{prompt['id']}. "
            f"[{prompt['category']}] "
            f"{prompt['title']} ⭐"
        )

    print(f"\n총 {len(favorite_prompts)}개의 즐겨찾기")

def export_prompts_to_markdown(prompt_list, categories):
    """전체 프롬프트를 카테고리별 Markdown 파일로 내보낸다."""
    print("\n=== 카테고리별 Markdown 내보내기 ===")

    EXPORT_DIR.mkdir(exist_ok=True)
    exported_count = 0

    for category in categories:
        category_prompts = [
            prompt
            for prompt in prompt_list
            if prompt["category"] == category
        ]

        if not category_prompts:
            continue

        file_name = f"{category.replace(' ', '_')}.md"
        file_path = EXPORT_DIR / file_name

        markdown_lines = [
            f"# {category} 프롬프트",
            "",
            f"총 {len(category_prompts)}개의 프롬프트",
            "",
        ]

        for prompt in category_prompts:
            favorite_mark = " ⭐" if prompt["favorite"] else ""
            favorite_text = "예" if prompt["favorite"] else "아니오"

            markdown_lines.extend(
                [
                    f"## {prompt['id']}. {prompt['title']}{favorite_mark}",
                    "",
                    f"- 카테고리: {prompt['category']}",
                    f"- 즐겨찾기: {favorite_text}",
                    "",
                    prompt["content"],
                    "",
                    "---",
                    "",
                ]
            )

        try:
            file_path.write_text(
                "\n".join(markdown_lines),
                encoding="utf-8",
            )
        except OSError as error:
            print(f"'{file_name}' 저장 중 오류가 발생했습니다: {error}")
            continue

        print(f"- {file_path}")
        exported_count += 1

    if exported_count == 0:
        print("내보낼 프롬프트가 없습니다.")
        return

    print(f"\n총 {exported_count}개의 Markdown 파일을 생성했습니다.")

def update_prompt(prompt_list, categories):
    """선택한 프롬프트의 제목, 내용, 카테고리를 수정한다."""
    print("\n=== 프롬프트 수정 ===")

    prompt_id_text = get_required_input("수정할 프롬프트 번호")

    if not prompt_id_text.isdigit():
        print("프롬프트 번호는 숫자로 입력해 주세요.")
        return

    prompt_id = int(prompt_id_text)
    selected_prompt = find_prompt_by_id(prompt_list, prompt_id)

    if selected_prompt is None:
        print("해당 번호의 프롬프트가 없습니다.")
        return

    print("\n현재 프롬프트 정보")
    print(f"제목: {selected_prompt['title']}")
    print(f"내용: {selected_prompt['content']}")
    print(f"카테고리: {selected_prompt['category']}")
    print("\n변경하지 않을 항목은 Enter만 누르세요.")

    new_title = input("새 제목: ").strip()
    new_content = input("새 내용: ").strip()

    print("\n새 카테고리 선택")
    print("0. 기존 카테고리 유지")

    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        category_choice = input("카테고리 번호: ").strip()

        if category_choice == "0":
            new_category = selected_prompt["category"]
            break

        if category_choice.isdigit():
            category_index = int(category_choice) - 1

            if 0 <= category_index < len(categories):
                new_category = categories[category_index]
                break

        print("올바른 카테고리 번호를 입력해 주세요.")

    changed = False

    if new_title and new_title != selected_prompt["title"]:
        selected_prompt["title"] = new_title
        changed = True

    if new_content and new_content != selected_prompt["content"]:
        selected_prompt["content"] = new_content
        changed = True

    if new_category != selected_prompt["category"]:
        selected_prompt["category"] = new_category
        changed = True

    if not changed:
        print("변경된 내용이 없습니다.")
        return

    save_prompts(prompt_list)
    print("프롬프트를 수정했습니다.")

def delete_prompt(prompt_list):
    """선택한 프롬프트를 확인 후 삭제한다."""
    print("\n=== 프롬프트 삭제 ===")

    prompt_id_text = get_required_input("삭제할 프롬프트 번호")

    if not prompt_id_text.isdigit():
        print("프롬프트 번호는 숫자로 입력해 주세요.")
        return

    prompt_id = int(prompt_id_text)
    selected_prompt = find_prompt_by_id(prompt_list, prompt_id)

    if selected_prompt is None:
        print("해당 번호의 프롬프트가 없습니다.")
        return

    print(f"\n삭제 대상: {selected_prompt['title']}")

    confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()

    if confirm != "y":
        print("삭제를 취소했습니다.")
        return

    prompt_list.remove(selected_prompt)
    save_prompts(prompt_list)

    print("프롬프트를 삭제했습니다.")

def show_top_prompts(prompt_list):
    """조회수가 높은 프롬프트를 최대 3개까지 출력한다."""
    print("\n=== 조회수 Top 프롬프트 ===")

    viewed_prompts = [
        prompt
        for prompt in prompt_list
        if prompt.get("views", 0) > 0
    ]

    if not viewed_prompts:
        print("아직 조회된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(
        viewed_prompts,
        key=lambda prompt: (-prompt.get("views", 0), prompt["id"]),
    )

    top_prompts = sorted_prompts[:3]

    for rank, prompt in enumerate(top_prompts, start=1):
        favorite_mark = " ⭐" if prompt["favorite"] else ""

        print(
            f"{rank}위. "
            f"[{prompt['category']}] "
            f"{prompt['title']}{favorite_mark} "
            f"- 조회수 {prompt.get('views', 0)}회"
        )

def wait_for_menu():
    """출력 내용을 확인한 후 메뉴로 돌아가도록 기다린다."""
    input("\n출력 내용을 확인한 뒤 Enter를 누르면 메뉴로 돌아갑니다.")

def show_menu():
    """프로그램의 메인 메뉴를 출력한다."""
    print("\n=== 반려동물 추억 콘텐츠 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. 카테고리별 Markdown 내보내기")
    print("9. 프롬프트 수정")
    print("10. 프롬프트 삭제")
    print("11. 조회수 Top 프롬프트")
    print("0. 종료")


def main():
    """사용자의 메뉴 선택을 반복해서 처리한다."""
    load_prompts(prompts)

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts, CATEGORIES)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_by_category(prompts, CATEGORIES)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            export_prompts_to_markdown(prompts, CATEGORIES)
        elif choice == "9":
            update_prompt(prompts, CATEGORIES)
        elif choice == "10":
            delete_prompt(prompts)
        elif choice == "11":
            show_top_prompts(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴 번호를 입력해 주세요.")

        wait_for_menu()


if __name__ == "__main__":
    main()