#!/bin/sh -e

current_dir=$(readlink -f .)
if [ "$(basename $current_dir)" != "deps" ] \
		|| ! grep -q 'AC_INIT(ejabberd' ../configure.ac  ; then

	echo "This script should be run in the ejabberd 'deps' directory"
	exit 1
fi

if [ ! -e ../config.status ] ; then
	echo "You should first run ./configure with all wanted options."
	exit 1
fi

rm -f .got || :
for dir in * ; do
	[ -d "$dir" ] || continue
	rm -rf "$dir"
done

cd ..
./rebar get-deps
cd deps

nr=10
for dir in * ; do
	[ -d "$dir" ] || continue
	cd $dir
	date=$(git log --format='%cd' --date=short -1 | tr -d '-')
	git archive --format=tar --prefix="deps/$dir/" HEAD \
		| gzip -9 > "../ejabberd-$dir-$date.tar.gz"
	cd ..
	echo -e "Source${nr}:\tejabberd-$dir-$date.tar.gz"
	echo -e "# Source${nr}-md5:\t$(set -- $(md5sum "ejabberd-$dir-$date.tar.gz"); echo $1)"
	nr=$((nr+1))
done
