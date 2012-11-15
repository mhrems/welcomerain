
from django.core.paginator import Paginator
class ObjectPaginator():
    pass
    def __init__(self,object,numberOfPage=2):
        self.object = object
        self.numberOfPage = numberOfPage
        self.paginatorObject = self.createPaginator()
        self.currentPage = 1
        
    def createPaginator(self):
        return Paginator(self.object,self.numberOfPage)
    
    def getObjectInPage(self,nPage):
       
        self.currentPage = self.getPageNumber(int(nPage))
        
        return self.paginatorObject.page(self.currentPage).object_list

    def getPageRange(self):
        return self.paginatorObject.page_range
    
    def getTotalPageNumber(self):
        return int(self.paginatorObject.num_pages)
    
    def getPageNumber(self,nPage):
        
        if nPage < 1:
            
            return 1
        elif self.getTotalPageNumber() < nPage :
     
            return self.getTotalPageNumber()
        return nPage
    
    def getCurrentPage(self):
        return int(self.currentPage)
        