class LoongTu:

    def __init__(self) -> None:
        self.name = "Prayut"
        self.lastname = "Chanocha"
        self.nickname = "Loong tu"
    
    def WhoIAm(self):
        # document of function
        '''
        This is a function for display information on this class
        '''
        print(f"My name is: {self.name}")
        print(f"My name is: {self.lastname}")
        print(f"My name is: {self.nickname}")

    @property
    def email(self):
        return "{}.{}@gmail.com".format(self.name, self.lastname).lower()
    
    @property
    def thainame(self):
        return "ประยุทธ์ จันทร์โอชา"
    
    def __str__(self):
        return 'This is a Loongtu class'


if __name__ == "__main__":
    myloong = LoongTu()
    print(myloong)
    print(myloong.name)
    print(myloong.lastname)
    print(myloong.nickname)
    myloong.WhoIAm()
    print("----------")
    mypaa = LoongTu()
    mypaa.name = "Somsri"
    mypaa.lastname = "Konthai"
    mypaa.nickname = "Sri"
    print(mypaa.name)
    print(mypaa.lastname)
    print(mypaa.nickname)
    mypaa.WhoIAm()
    print(mypaa.email)