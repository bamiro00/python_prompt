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
    }

    prompt_list.append(new_prompt)

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
    print("0. 종료")


def main():
    """사용자의 메뉴 선택을 반복해서 처리한다."""
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts, CATEGORIES)
        elif choice == "2":
            show_list(prompts)
        elif choice in {"3", "4", "5", "6", "7"}:
            print("해당 기능은 다음 단계에서 구현합니다.")
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴 번호를 입력해 주세요.")


if __name__ == "__main__":
    main()