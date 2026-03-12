#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b
    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    """Somador completo de 1 bit.

    Args:
        a: Primeira entrada de 1 bit.
        b: Segunda entrada de 1 bit.
        c: Carry de entrada.
        soma: Saida de soma.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        soma.next = a ^ b ^ c
        carry.next = (a & b) | (c & (a ^ b)) 
    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders, gerando
    uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits.
        y: Vetor de entrada de 2 bits.
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """
    c1 = Signal(bool(0)) 

    fa0 = fullAdder(
        a=x[0],
        b=y[0],
        c=0,
        soma=soma[0],
        carry=c1)

    fa1 = fullAdder(
        a=x[1],
        b=y[1],
        c=c1,
        soma=soma[1],
        carry=carry)
    return instances()



@block
def adder(x, y, soma, carry):

    n = len(x)

    # carries internos (n-1 apenas)
    carries = [Signal(bool(0)) for _ in range(n-1)]
    faList = [None for _ in range(n)]
    for i in range(n):

        if i == 0:
            cin = Signal(bool(0))   # carry inicial
        else:
            cin = carries[i-1]

        if i == n-1:
            cout = carry            # último vai para carry final
        else:
            cout = carries[i]

        faList[i] = fullAdder(
            a=x[i],
            b=y[i],
            c=cin,
            soma=soma[i],
            carry=cout)
    return instances()


@block
def addervb(x, y, soma, carry):
    """Somador vetorial em estilo comportamental.

    Versao combinacional que pode usar operacoes aritmeticas diretas
    sobre os vetores para gerar soma e carry.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        n = len(soma)
        result = intbv(0)[n+1:]
        result[:] = x + y
        soma.next = result[n:0]
        carry.next = result[n]
    return instances()
