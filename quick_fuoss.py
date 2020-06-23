import cctk, math, argparse, sys

def kd_formula(r1, r2, dielectric, temp=298):
    """
    Applies the Fuoss formula to model dissociation constants of spherical ions.
    Note that as written this formula is applicable only to charge ±1 ions!

    Args:
        r1 (float): radius of first ion in Å
        r2 (float): radius of second ion in Å
        dielectric (float): dielectric constant of solvent
        temp (float): temperature in Kelvin

    Returns:
        dissociation constant
    """
    assert isinstance(r1, (float, int)), "Need numeric value for r1!"
    assert isinstance(r2, (float, int)), "Need numeric value for r1!"
    assert isinstance(dielectric, (float, int)), "Need numeric value for dielectric!"
    assert isinstance(temp, (float, int)), "Need numeric value for temperature!"

    x = (r1 + r2) * 10 ** -8 # convert to cm

    N = 6.023 * 10 ** 23 # mol^-1
    e = 4.8 * 10 ** -10 # esu
    k = 1.38 * 10 ** -16 # erg/degree

    b = e ** 2 / (x * dielectric * k * temp)
    K = 3000 * math.exp(-1 * b) / (4 * math.pi * N * (x ** 3))

    return K

#### USAGE:
#### python quick_fuoss.py cation-name anion-name dielectric-constant
#### python quick_fuoss.py --type xyzfile cation.xyz anion.xyz dielectric-constant

parser = argparse.ArgumentParser(prog="quick_fuoss.py")
parser.add_argument("--type", "-t", type=str, default="name")
parser.add_argument("--temp", default=298, type=float)
parser.add_argument("cation")
parser.add_argument("anion")
parser.add_argument("dielectric", type=float)

args = vars(parser.parse_args(sys.argv[1:]))

m1, m2 = None, None

if args["type"] == "name":
    print("Reading from rdkit...")
    m1 = cctk.Molecule.new_from_name(args["cation"])
    m2 = cctk.Molecule.new_from_name(args["anion"])
elif args["type"] == "xyzfile":
    m1 = cctk.XYZFile.read_file(args["cation"]).molecule
    m2 = cctk.XYZFile.read_file(args["anion"]).molecule
else:
    print(f"Can't recognize ``type`` {args['type']} -- allowed values are ``name`` and ``xyzfile``!")

v1 = m1.volume()
v2 = m2.volume()
r1 = (0.75 * v1 / math.pi ) ** (1/3)
r2 = (0.75 * v2 / math.pi ) ** (1/3)

Kd = kd_formula(r1, r2, args["dielectric"], args["temp"])
print(f"Dissociation constant:\t{Kd:.8f} M")
