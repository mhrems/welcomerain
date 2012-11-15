import os
import logging

logger = logging.getLogger('wr.custom')

def logAddLine():
    logger.info('--------------------------------------------------------------')
    
    
def logInfo(msg,title=''):
    if title:
        logAddLine()
        logger.info(title)
    logger.info(msg)

def logWarning(msg):
    logger.warning(msg)

def logError(msg):
    logger.error(msg)

if __name__ == '__main__':
    print "mhrlog"