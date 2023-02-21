import argparse


def calc_tipi_j(ans):
    '''
    外向性			 ＝ （項目１ ＋ （８ – 項目６））／２
    協調性			 ＝ （（８ – 項目２） ＋ 項目７）／２
    勤勉性           ＝ （項目３ ＋ （８ – 項目８））／２
    神経症傾向       ＝ （項目４ ＋ （８ – 項目９））／２
    開放性			 ＝ （項目５ ＋ （８ – 項目 10））／２
    '''
    E = int((ans[0] + (8 - ans[5])) / 2)
    A = int(((8 - ans[1]) + ans[6]) / 2)
    C = int((ans[2] + (8 - ans[7])) / 2)
    N = int((ans[3] + (8 - ans[8])) / 2)
    O = int((ans[4] + (8 - ans[9])) / 2)

    return E, A, C, N, O


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='argparseTest',  # プログラム名
        usage='Demonstration of argparser',  # プログラムの利用方法
        description='description',  # 引数のヘルプの前に表示
        epilog='end',  # 引数のヘルプの後で表示
        add_help=True,  # -h/–help オプションの追加
    )
    
    # 引数の追加
    parser.add_argument('-a', '--answer')

    # 引数を解析する
    args = parser.parse_args()

    if args.answer:
        ans = [int(i) for i in args.answer.split(",")]
        
        E, A, C, N, O = calc_tipi_j(ans)
        print(E, A, C, N, O)