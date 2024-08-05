denna script används på arbetsformedlingen platsbanken annoser för att scrapa jobb infomationen som behövs för Aktivitetsrapportera 
detta är infon som sparas i ett xslx fil (URL", "Title", "Företag", "Arbetsroll", "Kommun", "Annons ID", "Datum") om filen inte finns så skapas en xslx fil med den nuvarande år och månads datum som namn.
scripten kan också söka nyckelord på annosen och skapa en prompt som kan användas med chatGPT/copilot för att ändra ditt personliga brev.

för att förstår denna script rekommenderas att man lär sig lite selenium och openpyxl (om man vill ändra excel managern)
för att selenium ska kunna använda chrome behövs en chrome driver som kan laddas ner här https://googlechromelabs.github.io/chrome-for-testing/ (jag använder 127.0.6533.88 just nu)
placera drivern i denna path "PATH = "C:\Program Files (x86)\chromedriver.exe""
för selenium är detta en bra tutorial
https://www.youtube.com/watch?v=j7VZsCCnptM&t=121s&pp=ygURc2VsZW5pdW0gdHV0b3JpYWw%3D
