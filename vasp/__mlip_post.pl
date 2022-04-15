#!/usr/bin/perl

open($fspec, "__mlip_species") or die "Cannot open __mlip_species";

$s = <$fspec>;

@spec_map = ();

while ($s =~ /^\s*(\d+)\s*(.*)$/) {
  push @spec_map, $1;
  $s = $2;
}

open($foutcar, "outcar.cfg") or die "Cannot open outcar.cfg";
open($f_outcar, ">", "_outcar.cfg") or die "Cannot open _OUTCAR for writing";

for($s = <$foutcar>;not($s =~ "AtomData:  id type");$s = <$foutcar>) {if(not($s)) {die "Broken outcar.cfg";} print $f_outcar $s;}
print $f_outcar $s;

for($s = <$foutcar>;$s =~ /^\s*(\d+)\s+(\d+)\s+(.*)$/;$s = <$foutcar>) {print $f_outcar $1." ".$spec_map[$2]." ".$3."\n";}

print $f_outcar $s;

while($s = <$foutcar>) {
print $f_outcar $s;
}

close $foutcar;
close $f_outcar;

unlink "outcar.cfg"
