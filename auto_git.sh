# sysinfo_page - A script to produce an html file

echo -n 'Type ur password: '
read -s text


if [ "$text" == "moon" ]; then
	echo
	echo -n "Your commit's message: "
	read text
	
	git add .
	git commit -m $text
	git push
	echo "tmquoc95@gmail.com"
fi



#echo tmquoc95@gmail.com
#echo 
