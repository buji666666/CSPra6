class VMTranslator:

    @staticmethod
    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        if segment == "constant":
            return f"@{offset}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment in ["local", "argument", "this", "that"]:
            seg_address = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
            return f"@{seg_address[segment]}\nD=M\n@{offset}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "static":
            return f"@{offset}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "pointer":
            return f"@{3 + offset}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "temp":
            return f"@{5 + offset}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        return ""

    @staticmethod
    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        if segment in ["local", "argument", "this", "that"]:
            seg_address = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
            return f"@{seg_address[segment]}\nD=M\n@{offset}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "static":
            return f"@SP\nAM=M-1\nD=M\n@{offset}\nM=D\n"
        elif segment == "pointer":
            return f"@SP\nAM=M-1\nD=M\n@{3 + offset}\nM=D\n"
        elif segment == "temp":
            return f"@SP\nAM=M-1\nD=M\n@{5 + offset}\nM=D\n"
        return ""

    @staticmethod
    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n"

    @staticmethod
    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"

    @staticmethod
    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        return "@SP\nA=M-1\nM=-M\n"

    @staticmethod
    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            "@TRUE\nD;JEQ\nD=0\n@SP\nA=M-1\nM=D\n@END_EQ\n0;JMP\n"
            "(TRUE)\nD=-1\n@SP\nA=M-1\nM=D\n(END_EQ)\n"
        )

    @staticmethod
    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            "@TRUE\nD;JGT\nD=0\n@SP\nA=M-1\nM=D\n@END_GT\n0;JMP\n"
            "(TRUE)\nD=-1\n@SP\nA=M-1\nM=D\n(END_GT)\n"
        )

    @staticmethod
    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            "@TRUE\nD;JLT\nD=0\n@SP\nA=M-1\nM=D\n@END_LT\n0;JMP\n"
            "(TRUE)\nD=-1\n@SP\nA=M-1\nM=D\n(END_LT)\n"
        )

    @staticmethod
    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n"

    @staticmethod
    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n"

    @staticmethod
    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        return "@SP\nA=M-1\nM=!M\n"

    @staticmethod
    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        return f"({label})\n"

    @staticmethod
    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        return f"@{label}\n0;JMP\n"

    @staticmethod
    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        return (
            "@SP\nAM=M-1\nD=M\n"
            f"@{label}\nD;JNE\n"
        )

    @staticmethod
    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        return (
            f"({function_name})\n" +
            "\n".join(["@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" for _ in range(n_vars)])
        )

    @staticmethod
    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return (
            f"@{function_name}$ret\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" +
            "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" +  
            "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" +  
            "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" +  
            "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" +  
            "@SP\nD=M\n@5\nD=D-A\n@ARG\nM=D\n" +  
            "@SP\nD=M\n@LCL\nM=D\n" +  
            f"@{function_name}\n0;JMP\n" +
            f"({function_name}$ret)\n"  
        )

    @staticmethod
    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return (
            "@LCL\nD=M\n@R13\nM=D\n" +  
            "@5\nA=D-A\nD=M\n@R14\nM=D\n" +  
            "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n" +  
            "@ARG\nD=M+1\n@SP\nM=D\n" +  
            "@R13\nD=M\n@1\nA=D-A\nD=M\n" +  
            "@THAT\nM=D\n" +
            "@R13\nD=M\n@2\nA=D-A\nD=M\n" +  
            "@THIS\nM=D\n" +
            "@R13\nD=M\n@3\nA=D-A\nD=M\n" +  
            "@ARG\nM=D\n" +
            "@R13\nD=M\n@4\nA=D-A\nD=M\n" +  
            "@LCL\nM=D\n" +
            "@R14\nA=M\n0;JMP\n" 
        )

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if len(tokens) == 1:
                    if tokens[0] == 'add':
                        print(VMTranslator.vm_add())
                    elif tokens[0] == 'sub':
                        print(VMTranslator.vm_sub())
                    elif tokens[0] == 'neg':
                        print(VMTranslator.vm_neg())
                    elif tokens[0] == 'eq':
                        print(VMTranslator.vm_eq())
                    elif tokens[0] == 'gt':
                        print(VMTranslator.vm_gt())
                    elif tokens[0] == 'lt':
                        print(VMTranslator.vm_lt())
                    elif tokens[0] == 'and':
                        print(VMTranslator.vm_and())
                    elif tokens[0] == 'or':
                        print(VMTranslator.vm_or())
                    elif tokens[0] == 'not':
                        print(VMTranslator.vm_not())
                    elif tokens[0] == 'return':
                        print(VMTranslator.vm_return())
                elif len(tokens) == 2:
                    if tokens[0] == 'label':
                        print(VMTranslator.vm_label(tokens[1]))
                    elif tokens[0] == 'goto':
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif tokens[0] == 'if-goto':
                        print(VMTranslator.vm_if(tokens[1]))
                elif len(tokens) == 3:
                    if tokens[0] == 'push':
                        print(VMTranslator.vm_push(tokens[1], int(tokens[2])))
                    elif tokens[0] == 'pop':
                        print(VMTranslator.vm_pop(tokens[1], int(tokens[2])))
                    elif tokens[0] == 'function':
                        print(VMTranslator.vm_function(tokens[1], int(tokens[2])))
                    elif tokens[0] == 'call':
                        print(VMTranslator.vm_call(tokens[1], int(tokens[2])))
