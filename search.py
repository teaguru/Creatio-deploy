import os
import shutil
# укажем где искать
os.chdir("c:\\")
i = 1
for root, dirs, files in os.walk(".", topdown = False):
    
   for name in files:
      # тут задано условие поиска
      if name == 'Microsoft.AspNet.OData.dll' or name == 'Microsoft.AspNet.OData.DLL':
          
        filex = os.path.join(root, name)
        # уберем из поиска то, что мы уже сложили в новую папку, чтобы небыло дублей
        if str(filex).find('Support') == -1:
            print(filex)
        
            # определим, куда ложить результаты
            os.makedirs('c:\\Support3\\{}'.format(i))
            shutil.copy2(filex, r'c:\\Support3\\{}'.format(i))
            x = open('c:\\Support3\\{}\\path.txt'.format(i),'tw')
            x.write(filex)
            x.close()
            i = i + 1
   for name in dirs:
       pass