import numpy as np
import struct
from pathlib import Path


def float32_to_hex_word(x: float) -> str:
    """
    Convert a Python/NumPy float to IEEE754 single-precision hex word.
    Returns 8 hex digits, e.g. 1.0 -> '3f800000'
    """
    b = struct.pack(">f", np.float32(x))  # big-endian byte order for text hex word
    return b.hex()


def matrix_to_word_mem(
    matrix: np.ndarray, out_path: str, *, row_major: bool = True
) -> None:
    """
    Convert an n x n NumPy matrix into a .mem file with:
      - one float32 word per line
      - each line = 8 hex digits
      - compatible with Verilog $readmemh directly into reg [31:0] mem[]

    Parameters
    ----------
    matrix : np.ndarray
        Input n x n matrix
    out_path : str
        Output .mem file path
    row_major : bool
        True  -> flatten as A[0,0], A[0,1], ...
        False -> flatten as A[0,0], A[1,0], ...
    """
    arr = np.asarray(matrix, dtype=np.float32)

    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"Expected n x n matrix, got shape {arr.shape}")

    flat = arr.ravel(order="C" if row_major else "F")

    out_file = Path(out_path)
    with out_file.open("w") as f:
        for val in flat:
            f.write(float32_to_hex_word(float(val)) + "\n")

    print(f"Wrote {flat.size} words to {out_file}")
    print(f"Matrix shape: {arr.shape}")
    print(f"Flatten order: {'row-major' if row_major else 'column-major'}")


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 3.0, 2.0, 1.0],
            [3.0, 5.0, 1.5, -2.0],
            [2.0, 1.5, 6.0, 0.5],
            [1.0, -2.0, 0.5, 7.0],
        ],
        dtype=np.float32,
    )

    matrix_to_word_mem(A, "matrix_words.mem", row_major=True)
