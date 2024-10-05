load AddSub.vm,
output-file AddSubTest2.out,
compare-to AddSubTest2.cmp,
output-list sp%D1.6.1 local%D1.6.1 argument%D1.8.1 this%D1.6.1 that%D1.6.1
            RAM[16]%D1.6.1 RAM[17]%D1.6.1 RAM[18]%D1.6.1
            local[0]%D1.8.1 local[1]%D1.8.1 local[2]%D1.8.1
            argument[0]%D1.11.1 argument[1]%D1.11.1 argument[2]%D1.11.1;

set sp 256,         // stack pointer
set local 700,      // base address of the local segment
set argument 800,   // base address of the argument segment
set this 3100,      // base address of the this segment
set that 3110,      // base address of the that segment

set RAM[16] 8,      // static 0 (x)
set RAM[17] 9,      // static 1
set RAM[18] 10,     // static 2

set local[0] 30,    // local 0 (a)
set local[1] 40,    // local 1 (b)
set local[2] 50,    // local 2

set argument[0] 120, // argument 0
set argument[1] 220, // argument 1
set argument[2] 320; // argument 2

repeat 25 {         // Execute 25 VM commands
  vmstep;
}
output;