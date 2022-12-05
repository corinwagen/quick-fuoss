import sys, argparse, math
import quick_fuoss

#### USAGE:
#### python quick_fuoss.py cation-name anion-name dielectric-constant

parser = argparse.ArgumentParser(prog="quick_fuoss.py")
parser.add_argument("--temp", default=298, type=float)
parser.add_argument("cation")
parser.add_argument("anion")
parser.add_argument("dielectric", type=float)

args = vars(parser.parse_args(sys.argv[1:]))
Kd = quick_fuoss.compute_kd(args["cation"], args["anion"], args["dielectric"], temp=args["temp"], verbose=True)

print(f"Dissociation constant:\t{Kd:.8f} M")

G = -0.001987 * args["temp"] * math.log(Kd)
print(f"Ionization energy: {G:.3f} kcal/mol")
