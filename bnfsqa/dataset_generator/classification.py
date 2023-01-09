import argparse
import sklearn.datasets as dt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description='Generate a synthetic sata for classification')
    parser.add_argument('n_samples', type=int, help='Number of samples')
    parser.add_argument('n_features', type=int, help='Number of features')
    parser.add_argument('n_redundant', type=int,
                        help='Number of redundant features')
    parser.add_argument('n_repeated', type=int,
                        help='Number of repeated features')
    parser.add_argument('class_sep', type=float,
                        help='Specifies whether different classes should be more spread out and easier to discriminate')
    parser.add_argument('output_path', type=str,
                        help='Specifies the path to save the results')
    args = parser.parse_args()
    rand_state = 0

    x, y = dt.make_classification(n_samples=args.n_samples,
                                  n_features=args.n_features,
                                  n_redundant=args.n_redundant,
                                  n_repeated=args.n_repeated,
                                  class_sep=args.class_sep,
                                  random_state=rand_state)

    df = pd.DataFrame(x)
    df['TARGET'] = pd.Series(y)
    for i in range(args.n_features):
        df.columns.values[i] = "A"+str(i)
    print(df)
    df.to_csv(args.output_path, index=False)


if __name__ == '__main__':
    main()
