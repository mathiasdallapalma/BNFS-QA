import argparse
import sklearn.datasets as dt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(
        description='Generate a synthetic sata for regression')
    parser.add_argument('n_samples', type=int, help='Number of samples')
    parser.add_argument('n_features', type=int, help='Number of features')
    parser.add_argument('n_informative', type=int,
                        help='Number of informative features')
    parser.add_argument('noise', type=float,
                        help='The standard deviation of the gaussian noise applied to the output.')
    parser.add_argument('bias', type=float,
                        help='Specifies the bias term in the underlying linear model')
    parser.add_argument('output_path', type=str,
                        help='Specifies the path to save the results')
    args = parser.parse_args()
    rand_state = 0

    x, y = dt.make_regression(n_samples=args.n_samples,
                              n_features=args.n_features,
                              n_informative=args.n_informative,
                              noise=args.noise,
                              bias=args.bias,
                              random_state=rand_state)

    df = pd.DataFrame(x)
    df['TARGET'] = pd.Series(y)
    for i in range(args.n_features):
        df.columns.values[i] = "A"+str(i)
    print(df)
    df.to_csv(args.output_path, index=False)


if __name__ == '__main__':
    main()
