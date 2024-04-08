def find_year(mis):
            if mis.startswith("6122"):
                year="Second Year"
                return year
            elif mis.startswith("6123"):
                year="First Year"
                return year
            elif mis.startswith("1121"):
                year="Third Year"
                return year
            elif mis.startswith("1120"):
                 year="Final Year"
                 return year
            elif mis.startswith("6422"):
                 year="Second Year"
                 return year
            elif mis.startswith("6423"):
                 year="First Year"
                 return year
            elif mis.startswith("1421"):
                 year="Third Year"
                 return year
            elif mis.startswith("1420"):
                 year="Final  Year"
                 return year
             
def find_branch(mis):
        if mis[5]=='1':
            branch="CIVIL"
            return branch
        elif mis[5]=='3'and mis[4]=='0':
            branch="COMPUTER"
            return branch
        elif mis[5]=='5':
            branch="ELECTRICAL"
            return branch
        elif mis[5]=='7':
            branch="ENTC"
            return branch
        elif mis[5]=='9':
            branch="INSTRU"
            return branch
        elif mis[5]=='3'and mis[4]=='1':
            branch="MANUFACTURING"
            return branch
        elif mis[5]=='0':
            branch="MECHANICAL"
            return branch
        elif mis[5]=='1'and mis[4]=='1':
            branch="METALLARGY"
            return branch
        elif mis[5]=='4'and mis[4]=='1':
            branch="PLANNING"
            return branch