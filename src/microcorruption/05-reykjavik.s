2400 <login>
2400: 0b12           push	r11
2402: 0412           push	r4
2404: 0441           mov	sp, r4
2406: 2452           add	#0x4, r4
2408: 3150 e0ff      add	#0xffe0, sp
240c: 3b40 2045      mov	#0x4520, r11  "what's the password?"
2410: 073c           jmp	$+0x10 <#0x2420>
2412: 1b53           inc	r11
2414: 8f11           sxt	r15
2416: 0f12           push	r15
2418: 0312           push	#0x0  ; output
241a: b012 6424      call	#0x2464 <INT>
241e: 2152           add	#0x4, sp
2420: 6f4b           mov.b	@r11, r15
2422: 4f93           tst.b	r15
2424: f623           jnz	$-0x12 <#0x2412>
2426: 3012 0a00      push	#0xa  ; newline char
242a: 0312           push	#0x0  ; output
242c: b012 6424      call	#0x2464 <INT>
2430: 2152           add	#0x4, sp
2432: 3012 1f00      push	#0x1f
2436: 3f40 dcff      mov	#0xffdc, r15
243a: 0f54           add	r4, r15
243c: 0f12           push	r15
243e: 2312           push	#0x2  ; input
2440: b012 6424      call	#0x2464 <INT>
2444: 3150 0600      add	#0x6, sp
2448: b490 d077 dcff cmp	#0x77d0, -0x24(r4)
244e: 0520           jnz	$+0xc <#0x245a>
2450: 3012 7f00      push	#0x7f  ; unlock
2454: b012 6424      call	#0x2464 <INT>
2458: 2153           incd	sp
245a: 3150 2000      add	#0x20, sp
245e: 3441           pop	r4
2460: 3b41           pop	r11
2462: 3041           ret

2464 <INT>
2464: 1e41 0200      mov	0x2(sp), r14
2468: 0212           push	sr
246a: 0f4e           mov	r14, r15
246c: 8f10           swpb	r15
246e: 024f           mov	r15, sr
2470: 32d0 0080      bis	#0x8000, sr
2474: b012 1000      call	#0x10 <__trap_interrupt>
2478: 3241           pop	sr
247a: 3041           ret

247c: d21a 189a      call	&0x9a18
2480: 22dc           bis	@r12, sr
2482: 45b9           bit.b	r9, r5
2484: 4279           subc.b	r9, sr
2486: 2d55           add	@r5, r13
2488: 858e a4a2      sub	r14, -0x5d5c(r5)
248c: 67d7           bis.b	@r7, r7
248e: 14ae a119      dadd	0x19a1(r14), r4
2492: 76f6           and.b	@r6+, r6
2494: 42cb           bic.b	r11, sr
2496: 1c04 0efa      rrc	-0x5f2(r12)
249a: a61b           invalid	@r6
249c: 74a7           dadd.b	@r7+, r4
249e: 416b           addc.b	r11, sp
24a0: d237           jge	$-0x5a
24a2: a253 22e4      incd	&0xe422
24a6: 66af           dadd.b	@r15, r6
24a8: c1a5 938b      dadd.b	r5, -0x746d(sp)
24ac: 8971 9b88      subc	sp, -0x7765(r9)
24b0: fa9b 6674      cmp.b	@r11+, 0x7466(r10)
24b4: 4e21           jnz	$+0x29e
24b6: 2a6b           addc	@r11, r10
24b8: b143 9151      mov	#-0x1, 0x5191(sp)
24bc: 3dcc           bic	@r12+, r13
24be: a6f5 daa7      and	@r5, -0x5826(r6)
24c2: db3f           jmp	$-0x48
24c4: 8d3c           jmp	$+0x11c
24c6: 4d18           rrc.b	r13
24c8: 4736           jge	$-0x370
24ca: dfa6 459a 2461 dadd.b	-0x65bb(r6), 0x6124(r15)
24d0: 921d 3291      sxt	&0x9132
24d4: 14e6 8157      xor	0x5781(r6), r4
24d8: b0fe 2ddd      and	@r14+, -0x22d3(pc)
24dc: 400b           reti	pc
24de: 8688 6310      sub	r8, 0x1063(r6)
24e2: 3ab3           bit	#-0x1, r10
24e4: 612b           jnc	$-0x13c
24e6: 0bd9           bis	r9, r11
24e8: 483f           jmp	$-0x16e
24ea: 4e04           rrc.b	r14
24ec: 5870 4c38      subc.b	0x384c(pc), r8
24f0: c93c           jmp	$+0x194
24f2: ff36           jge	$-0x200
24f4: 0e01           rra	r14
24f6: 7f3e           jmp	$-0x300
