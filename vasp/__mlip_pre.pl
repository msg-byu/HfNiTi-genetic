#!/usr/bin/perl

# if (open($fh, "__mlip_species")) {die "Error: __mlip_species already exists"}

open($f_poscar, "_POSCAR") or die "Cannot open _POSCAR";
open($f_potcar, "_POTCAR") or die "Cannot open _POTCAR";
open($fposcar, ">", "POSCAR") or die "Cannot open POSCAR for writing";

for($i=0; $i<5; $i++) {$s = <$f_poscar>; print $fposcar $s;}
$s = <$f_poscar>;
if($s =~ /^\s*\d/) {} else {print $fposcar $s; $s = <$f_poscar>;}

# $s is species numbers

@orig_spec_count = ();
@spec_count = ();
@spec_map = ();

$i=0;

while ($s =~ /^\s*(\d+)\s*(.*)$/) {
  push @orig_spec_count, $1;
  if($1 != 0) {push @spec_count, $1; push @spec_map, $i;};
  $s = $2;
  $i = $i + 1;
}

$n = scalar @spec_count;
for ($i=0; $i<$n; $i++) {print $fposcar ' '.$spec_count[$i];}
print $fposcar "\n";
while($s = <$f_poscar>) {print $fposcar $s;}

open($fpotcar, ">", "POTCAR") or die "Cannot open POTCAR for writing";
for($i=0; $i<scalar @orig_spec_count; $i++) {
for($s = <$f_potcar>; not($s =~ /End of Dataset/); $s = <$f_potcar>) {if($orig_spec_count[$i] != 0) {if(not($s)) {die "_POTCAR has not enough pseudopotentials!"}; print $fpotcar $s;}}
if($orig_spec_count[$i] != 0) {print $fpotcar $s;}
}

close $fpotcar;
close $fposcar;

open($fspec, ">", "__mlip_species") or die "Cannot open __mlip_species for writing";

for ($i=0; $i<$n; $i++) {print $fspec ' '.$spec_map[$i];}

close $fspec;

# print "$species_removed species removed\n";
