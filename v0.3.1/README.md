要使一个彩票系统真正可信，开奖号码应该是真正意义上的随机数，不能被任何外界因素操控；彩票涉及的所有数据和开奖方法应对所有人透明可查；透过公开的数据和算法，任何人都可以验证最终开奖号码，证明其不受任何秘密的隐藏因素的影响。

其操作流程如图6-1彩票模型B所示，首先对彩票购买截止时间点内的所有售出的彩票号码数据排序，立即公开和公证该数据的哈希值(参见2、哈希算法简介)，并在随后提供原始数据的下载。

然后，把上一步计算得到的哈希值作为输入，使用一个可以消耗特定时间长度的公开算法（参见5、确定性时延算法），得到最终的开奖号码。对于一个特定的开奖算法来说，开奖号码由彩票池原始数据唯一确定。
