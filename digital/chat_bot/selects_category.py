from get_labor_law import get_labor_law 

def selects_category(user_message):

    if user_message in ["SODAに相談する" , "相談する" , "相談" , "SODA"]:
        reply_message = (
            "この中から選んでください。\n\n"
            "1,ハラスメント・職場環境\n"
            "2,解雇・退職・雇い止め\n"
            "3,雇用形態・契約トラブル\n"
            "4,賃金・給与\n"
            "5,就業時間・休暇\n"
            "6,社会保険・労働保険\n"
            "7,人事・評価・昇進\n"
            "8,労働組合・団体交渉\n"
            "9,安全衛生・労災\n"
            "10,その他（自由入力）\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["1", "１"]:
        reply_message = (
            "1,ハラスメント・職場環境ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "1A,パワーハラスメント\n"
            "1B,セクシャルハラスメント\n"
            "1C,マタニティーハラスメント\n"
            "1D,SOGIハラスメント（性的指向・性自認）\n"
            "1E,モラルハラスメント（精神的な嫌がらせ）\n"
            "1F,いじめ・嫌がらせ\n"
            "1G,職場環境改善\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["2", "２"]:
        reply_message = (
            "2,解雇・退職・雇い止めですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "2A,不当解雇\n"
            "2B,退職勧奨\n"
            "2C,雇い止め\n"
            "2D,退職手続き\n"
            "2E,退職金トラブル\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["3", "３"]:
        reply_message = (
            "3,雇用形態・契約トラブルですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "3A,正社員・契約社員・派遣社員の違い\n"
            "3B,契約更新・終了\n"
            "3C,副業・兼業\n"
            "3D,業務委託・フリーランス\n"
            "3E,試用期間のトラブル\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["4", "４"]:
        reply_message = (
            "4,賃金・給与ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "4A,給与未払い\n"
            "4B,残業代未払い\n"
            "4C,賞与・ボーナス\n"
            "4D,給与引き下げ\n"
            "4E,昇給・減給\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["5", "５"]:
        reply_message = (
            "5,就業時間・休暇ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "5A,残業・休日出勤\n"
            "5B,36協定・時間外労働\n"
            "5C,有給休暇\n"
            "5D,産休・育休\n"
            "5E,介護休暇\n"
            "5F,休職・復職\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["6", "６"]:
        reply_message = (
            "6,社会保険・労働保険ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "6A,健康保険\n"
            "6B,年金（厚生年金・国民年金）\n"
            "6C,失業保険（雇用保険）\n"
            "6D,労災保険\n"
            "6E,介護保険\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["7", "７"]:
        reply_message = (
            "7,人事・評価・昇進ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "7A,人事評価の不公平\n"
            "7B,昇進・降格\n"
            "7C,異動・転勤\n"
            "7D,研修・教育機会\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["8", "８"]:
        reply_message = (
            "8,労働組合・団体交渉ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "8A,労働組合の加入・活動\n"
            "8B,団体交渉の進め方\n"
            "8C,労働争議\n"
            "8D,労働協約・労働協定\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["9", "９"]:
        reply_message = (
            "9,安全衛生・労災ですね。\n\n"
            "もう少し詳しく聞きたいです。\n"
            "この中から選んでください。\n\n"
            "9A,労働環境の安全性\n"
            "9B,職場の健康管理\n"
            "9C,労災の認定\n"
            "9D,精神疾患・過労死問題\n\n"
            "上記以外の場合は自由に入力してください。"
        )

    elif user_message in ["10", "１０"]:
        reply_message = (
            "10,その他の相談ですね。\n\n"
            "自由にご記入ください。\n\n"
            "[SODAとは]\n"
            "https://www.notion.so/SODA-19ef6dbbf48380c892c9cd96c5322823"
        )

    else:
        reply_message = get_labor_law(user_message)

    return reply_message