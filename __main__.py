from bnslqa.solvers import exact_solver, dwave_solver


import argparse



def main():
    parser = argparse.ArgumentParser(description='Implementation of Bayesian Network Structure Learning using Quantum Annealing',
                                    )
    subparsers = parser.add_subparsers(help='sub-command help')

    discretizer_parser = subparsers.add_parser('discretize', help='discretize dataset',
                                            description='',
                                            epilog='Example:')
    discretizer_parser.add_argument('dataset', type=str, help='dataset path')
    discretizer_parser.add_argument('-b','--bind', type=int, metavar='NUM', default=5, help='')
    discretizer_parser.add_argument('-l','--labels', help='', metavar='ARRAY', nargs='+', default=[])
    discretizer_parser.add_argument('-t','--target', type=int, metavar='NUM', default=-1, help='')




    solver_parser = subparsers.add_parser('solve', help='estimate BN structure from data',
                                            description='',
                                            epilog='''Example: \'python -m bnslqa solve datasets/WasteExp.txt QA -r 10000 -a 99\'
                                            will use D-Wave\'s Quantum Annealer to solve the WasteExp problem, with 10000 reads
                                            each with an annealing time of 99 microseconds''')
    solver_parser.add_argument('dataset', type=str, help='dataset path') #TODO da ricalcolare se si usa pipenile

    solver_parser.add_argument('strategy', type=str, choices=['ES','SA','QA'],
                                help='strategy to be used (Exhaustive Search, Simulated Annealing, Quantum Annealing)') #TODO aggiungi metodi di bnlearn



    solver_parser.add_argument('-r','--reads', type=int, metavar='NUM', default=10**4,
                                help='number of reads for annealing strategies, SA has no limits, QA can have at most 10000 [default: 10000]')
    solver_parser.add_argument('-a','--anneal', type=int, metavar='T', default=99,
                                help='annealing time in microseconds for each read (only for QA), up to 2000 [default: 99]')


    args = parser.parse_args()

    
    if 'strategy' in args:
        if args.strategy == 'ES':
            func = exact_solver.main
        else:
            func = dwave_solver.main
    else:
        parser.print_usage()
        parser.exit(1)


    func(args)

if __name__ == '__main__':
  main()