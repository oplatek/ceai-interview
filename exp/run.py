#!/usr/bin/env python3
import argparse
import editdistance
from collections import defaultdict, Counter


class CounterModel:
    def __init__(self):
        self.stat = defaultdict(Counter)

    def learn(self, inp, gline):
        sinp = inp.split()
        sgline = gline.split()
        for iw, gw in zip(sinp, sgline):
            self.stat[iw][gw] += 1

    def predict(self, iline):
        res = []
        for w in iline.split():
            try:
                res.append(self.stat[w].most_common(1)[0][0])
            except IndexError:
                res.append('OOV')
        return ' '.join(res)


def infer(model, inp, gold):
    for iline, gline in zip(inp.splitlines(), gold.splitlines()):
        model.learn(iline, gline)


def eval_line(gold, hyp):
    return editdistance.eval(gold, hyp), len(gold)


def eval(model, inp, gold, compf):
    scores = []
    for iline, gline in zip(inp.splitlines(), gold.splitlines()):
        yline = model.predict(iline)
        print('gold:', gline, '\n', 'hyp: ', yline, '\n\n')
        score, chars = compf(gline, yline)
        scores.append(score)
    score = sum(scores) / len(scores)
    print(score)
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('train_input')
    parser.add_argument('train_gold')
    parser.add_argument('eval_input')
    parser.add_argument('eval_gold')
    args = parser.parse_args()

    with open(args.train_input, 'r') as train_in, open(args.train_gold, 'r') as train_g, open(args.eval_input, 'r') as eval_in, open(args.eval_gold, 'r') as eval_g:
        train_inp = train_in.read()
        train_gold = train_g.read()
        eval_inp = eval_in.read()
        eval_gold = eval_g.read()

        # train_inp = "zlutoucky kun"
        # train_gold = "žluťoučký kůň"
        model = CounterModel()
        infer(model, train_inp, train_gold)
        print(model.stat)
        eval(model, train_inp, train_gold, eval_line)
        eval(model, eval_inp, eval_gold, eval_line)
