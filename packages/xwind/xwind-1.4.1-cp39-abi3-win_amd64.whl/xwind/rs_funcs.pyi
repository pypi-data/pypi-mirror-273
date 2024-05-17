def v_k_2_c(v:float,k:float)->float:
    """风速和形状因子转换为尺度因子

    Args:
        v: 风速
        k: 形状因子

    Returns:
        尺度因子

    """
    pass

def c_k_2_v(c:float,k:float)->float:
    """
    通过尺度因子和形状因子计算风速值
    Args:
        c: 威布尔函数中的尺度因子，有时候也用A符号表示
        k: 威布尔函数中的形状因子

    Returns:
        风速值
    """
    pass
def wbl_cdf(c:float,k:float,v1:float,v2:float)->float:
    """
    计算威布尔函数某区间内的累积频率分布
    Args:
        c: 威布尔函数中的尺度因子，有时候也用A符号表示
        k: 威布尔函数中的形状因子
        v1: 风速区间左值
        v2: 风速区间右值

    Returns:
        float: 累积分布频率
    """
    pass
