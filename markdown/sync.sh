echo '              ------------ sync markdown  ----------'
if [ ! -e md ]; then
mkdir md
fi
svn co "http://10.1.55.36/svn/AndroidPF/04.SoftwareDevelopLibrary/03.SystemDesign(SD)/AndroidPF_Dev/02.InterfaceDefinition/markdown_doc" ./markdown/md/
#svn export --force "http://10.1.55.36/svn/AndroidPF/04.SoftwareDevelopLibrary/03.SystemDesign(SD)/AndroidPF_Dev/02.InterfaceDefinition/markdown_doc" ./md/
