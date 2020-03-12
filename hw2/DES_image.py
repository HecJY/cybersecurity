import BitVector

def image_encyption(image, round_key, output_f):
    file = open(image, "rb")
    file_out = open(output_f, "wb")

    image_info = file.readlines()
    file_out.writelines(image_info[0:3])

    file_out.close()

    image_bv = BitVector(filename = image)
    image_bv.read_bits_from_file(len(image_info[0:3])*8)

    while (image_bv.more_to_read):
        bitvec = image_bv.read_bits_from_file(64)
        if bitvec.size > 0:
            if len(bitvec) != 64:
                # fiil the array when the bit count is not 64
                bitvec.pad_from_right(64 - len(bitvec))
            # divide the left and right bit first, then put in the boxes
            [LE, RE] = bitvec.divide_into_two()
            for i in range(0, len(round_key)):
                newRE = RE.permute(expansion_permutation)
                out_xor = newRE ^ (round_key[i])

                # substition with the s-box
                sub = substitute(out_xor)

                # permutation with the expansion box
                permute_RE = sub.permute(pbox_permutation)

                # now switch the right and left side, update the left side
                RE_new = permute_RE ^ LE
                LE = RE
                RE = RE_new
            encrypted_text = LE + RE
            with open(output_f, "ab") as file_out:
                encrypted_text.write_to_file(file_out)