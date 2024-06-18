import subprocess as sp

partnum = [0]
output_name = [""]

def start(outputname):
    print(f"INFO: creating {outputname}.asm")
    output_name[0] = outputname
    with open(output_name[0] + ".asm", "w") as fi:
        fi.write("section .text\n")
        fi.write("    global _start\n")
        fi.write("\n")
        fi.write("end:\n")
        fi.write("    mov rax, 60\n")
        fi.write("    mov rdi, 0\n")
        fi.write("    syscall\n")
        fi.write("\n")
        fi.write("_start:\n")

def msg(message):
    message_len = len(message)
    partnum[0] += 1
    msg = message.replace("\\n", "")
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .data\n")
        if message.endswith("\\n"):
            fi.write(f"    msg_p{partnum[0]} db '{msg}', 10, 0\n")
        else:
            fi.write(f"    msg_p{partnum[0]} db '{message}', 0\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("    mov rax, 1\n")
        fi.write("    mov rdi, 1\n")
        fi.write(f"    mov rsi, msg_p{partnum[0]}\n")
        fi.write(f"    mov rdx, {message_len}\n")
        fi.write("    syscall\n")

def strinp(varname):
    partnum[0] += 1
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .bss\n")
        fi.write(f"    {varname} resb 128\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("    mov rax, 0\n")
        fi.write("    mov rdi, 0\n")
        fi.write(f"    mov rsi, {varname}\n")
        fi.write(f"    mov rdx, 128\n")
        fi.write("    syscall\n")

def prtinp(varname):
    partnum[0] += 1
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("    mov rax, 1\n")
        fi.write("    mov rdi, 1\n")
        fi.write(f"    mov rsi, {varname}\n")
        fi.write(f"    mov rdx, 128\n")
        fi.write("    syscall\n")

def createstrvar(varname, value):
    partnum[0] += 1
    value_len = len(value)
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .data\n")
        if value.endswith("\\n"):
            rplcedvalue = value.replace("\\n", "")
            fi.write(f"    {varname} db '{rplcedvalue}', 10, 0\n")
        else:
            fi.write(f"    {varname} db '{value}', 0\n")
        fi.write(f"    size_of_{varname} equ {value_len}\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("")

def prtvar(varname):
    partnum[0] += 1
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("    mov rax, 1\n")
        fi.write("    mov rdi, 1\n")
        fi.write(f"    mov rsi, {varname}\n")
        fi.write(f"    mov rdx, size_of_{varname}\n")
        fi.write("    syscall\n")

def strcpy(dest, src):
    partnum[0] += 1
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write(f"    mov rsi, {src}\n")
        fi.write(f"    mov rdi, {dest}\n")
        fi.write("copy_loop:\n")
        fi.write("    lodsb\n")
        fi.write("    stosb\n")
        fi.write("    test al, al\n")
        fi.write("    jnz copy_loop\n")

def asciimsg(asciinum):
    partnum[0] += 1
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write(f"    jmp part_{partnum[0]}\n")
        fi.write("section .data\n")
        fi.write(f"    msg_p{partnum[0]} db {asciinum}, 0\n")
        fi.write("section .text\n")
        fi.write(f"part_{partnum[0]}:\n")
        fi.write("    mov rax, 1\n")
        fi.write("    mov rdi, 1\n")
        fi.write(f"    mov rsi, msg_p{partnum[0]}\n")
        fi.write(f"    mov rdx, 1\n")
        fi.write("    syscall\n")

def end():
    with open(output_name[0] + ".asm", "a") as fi:
        fi.write("    jmp end\n")
    print(f"EXEC: nasm -felf64 -o {output_name[0]}.o {output_name[0]}.asm")
    sp.run(f"nasm -felf64 -o {output_name[0]}.o {output_name[0]}.asm", shell=True)
    print(f"EXEC: ld -o {output_name[0]} {output_name[0]}.o")
    sp.run(f"ld -o {output_name[0]} {output_name[0]}.o", shell=True)
    print(f"EXEC: rm -rf {output_name[0]}.o")
    sp.run(f"rm -rf {output_name[0]}.o", shell=True)
