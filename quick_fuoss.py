import cctk, math, argparse, sys, re

#### USAGE:
#### python quick_fuoss.py cation-name anion-name dielectric-constant

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

def compute_kd(mol1, mol2, dielectric, temp=298, verbose=False):
    mols = [None, None]
    for i, n in enumerate([mol1, mol2]):
        try:
            if re.search("xyz$", n):
                if verbose:
                    print(f"Reading ion #{i+1} from file {n}...")
                mols[i] = cctk.XYZFile.read_file(n).molecule
            else:
                if verbose:
                    print(f"Reading ion #{i+1} from rdkit...")
                mols[i] = cctk.Molecule.new_from_name(n)
        except Exception as e:
            print(f"Error reading molecule #{i+1}!\n{e}")

    v1 = mols[0].volume()
    v2 = mols[1].volume()
    r1 = (0.75 * v1 / math.pi ) ** (1/3)
    r2 = (0.75 * v2 / math.pi ) ** (1/3)

    Kd = kd_formula(r1, r2, dielectric, temp)
    return Kd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="quick_fuoss.py")
    parser.add_argument("--temp", default=298, type=float)
    parser.add_argument("cation")
    parser.add_argument("anion")
    parser.add_argument("dielectric", type=float)

    args = vars(parser.parse_args(sys.argv[1:]))
    Kd = compute_kd(args["cation"], args["anion"], args["dielectric"], temp=args["temp"], verbose=True)

    print(f"Dissociation constant:\t{Kd:.8f} M")
