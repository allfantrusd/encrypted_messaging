def caesarCipher(string:str,mode="encrypt"):

    ##set key and mode : weather encrypt or decrypt
    key  = 13
    symbol = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789 !?."
    encrypted =  ''
    for sym in string:
        if sym in symbol:
            sym_index = symbol.find(sym)
            if mode=="encrypt":
                translated_index = sym_index +key
            elif mode =="decrypt":
                translated_index = sym_index - key
            if translated_index >=len(symbol):
                translated_index -= len(symbol)
            elif translated_index <0 :
                translated_index +=len(symbol)
            encrypted += symbol[translated_index]
        else:
            encrypted +=symbol

    return encrypted
if __name__=="__main__":
    caesarCipher()