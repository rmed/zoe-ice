#!/usr/bin/env perl
#
# Zoe ICE
# https://github.com/rmed/zoe-ice
#
# Copyright (c) 2016 Rafael Medina García <rafamedgar@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

use Getopt::Long qw(:config pass_through);

my $get;
my $run;
my $sender;
my $locale;
my $src;

my $add_mails;
my $rm_mails;
my $enable;
my $disable;
my $get_date;
my $set_date;
my $get_msg;
my $set_msg;
my $get_ice;
my $test;

my $date;
my $string;
my @mails;

GetOptions("get"                   => \$get,
           "run"                   => \$run,
           "msg-sender-uniqueid=s" => \$sender,
           "msg-sender-locale=s"   => \$locale,
           "msg-src=s"             => \$src,

           "am"                    => \$add_mails,
           "rm"                    => \$rm_mails,
           "e"                     => \$enable,
           "d"                     => \$disable,
           "gd"                    => \$get_date,
           "sd"                    => \$set_date,
           "gm"                    => \$get_msg,
           "sm"                    => \$set_msg,
           "gi"                    => \$get_ice,
           "t"                     => \$test,

           "date=s"                => \$date,
           "string=s"              => \$string,
           "mail=s"                => \@mails);

if ($get) {
    &get;
} elsif ($run and $add_mails) {
    &add_mails;
} elsif ($run and $rm_mails) {
    &rm_mails;
} elsif ($run and $enable) {
    &enable;
} elsif ($run and $disable) {
    &disable;
} elsif ($run and $get_date) {
    &get_date;
} elsif ($run and $set_date) {
    &set_date;
} elsif ($run and $get_msg) {
    &get_msg;
} elsif ($run and $set_msg) {
    &set_msg;
} elsif ($run and $get_ice) {
    &get_ice;
} elsif ($run and $test) {
    &test;
}

sub get {
    # if ($locale and ($locale eq "es")) {
        # Spanish
		print("--am añade correos/mails ice/ICE <mail>\n");
		print("--rm elimina/quita correos/mails ice/ICE <mail>\n");
		print("--e activa ice/ICE\n");
		print("--d deshabilita ice/ICE\n");
		print("--gd dame/muestra /la fecha /del ice/ICE\n");
        print("--sd establece/cambia /la fecha /del ice/ICE /a <date>\n");
		print("--gm dame/muestra /el mensaje /del ice/ICE\n");
		print("--sm establece/cambia /el mensaje /del ice/ICE a <string>\n");
		print("--gi dame/muestra /un resumen /del ice/ICE\n");
		print("--t probar/prueba /mi ice/ICE\n");

    # } else {
        # English (default)
		print("--am add ice/ICE mails <mail>\n");
		print("--rm remove ice/ICE mails <mail>\n");
		print("--e enable ice/ICE\n");
		print("--d disable ice/ICE\n");
		print("--gd give /me ice/ICE date\n");
        print("--sd set ice/ICE date /to <date>\n");
		print("--gm give /me ice/ICE message\n");
		print("--sm set ice/ICE message to <string>\n");
		print("--gi show /me ice/ICE /summary\n");
		print("--t test /my ice/ICE\n");
    # }
}

# Add emails to ICE record
sub add_mails {
    print("message dst=ice&user=$sender&src=$src&tag=add-mails&emails=@mails\n");
}

# Remove emails from ICE record
sub rm_mails {
    print("message dst=ice&user=$sender&src=$src&tag=rm-mails&emails=@mails\n");
}

# Enable an ICE delivery
sub enable {
    print("message dst=ice&user=$sender&src=$src&tag=enable-ice\n");
}

# Disable an ICE delivery
sub disable {
    print("message dst=ice&user=$sender&src=$src&tag=disable-ice\n");
}

# Get current ICE date
sub get_date {
    print("message dst=ice&user=$sender&src=$src&tag=get-date\n");
}

# Set ICE date
sub set_date {
    print("message dst=ice&user=$sender&src=$src&tag=set-date&date=$date\n");
}

# Obtain current ICE message
sub get_msg {
    print("message dst=ice&user=$sender&src=$src&tag=get-msg\n");
}

# Set ICE message
sub set_msg {
    print("message dst=ice&user=$sender&src=$src&tag=set-msg&message=$string\n");
}

# Get a summary of the ICE
sub get_ice {
    print("message dst=ice&user=$sender&src=$src&tag=get-ice\n");
}

sub test {
    print("message dst=ice&user=$sender&src=$src&tag=test-ice\n");
}
