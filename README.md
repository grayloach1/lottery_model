# lottery_model
如何设计一套可证明的可信彩票系统


1、彩票的固有问题：以中国福利彩票为例（略）
优点
1.1 开奖过程直观
1.2 具有极高的认知度，是中国的绝对主流。
缺点
1.3 开奖号码不是真正的随机数。
1.4 彩票中心节点控制了所有流程，传统的流程处处皆漏洞，可信度低。
1.5 福彩贪腐严重，名声不好。

2、一个可信的彩票系统应该是怎样的
2.1 随机性：开奖号码是真正意义上的随机数，不存在潜在的未知方法可以改变这一点。
2.2 完备性：所有已购买的彩票号码是完整的，可查询的，不可修改的。
2.3 全透明：算法和数据皆可查询、可验证。
下面将由浅入深，依次介绍其操作流程、原理和算法，证明其可信性。

3、可信彩票系统操作流程
Step1 
对彩票购买时间截止点内的所有已销售彩票号码排序，称该数据为【彩票池】。立即公开和公证彩票池的数据指纹（也称哈希值），并在随后提供彩票池原始数据的下载。注意，需要确保在临近截止时间点之前有彩票购买记录。
Step2
把彩票池的数据指纹作为输入，使用一个可以消耗特定时间长度的公开的开奖算法，可以得到一组确定的开奖号码。对于这个特定的开奖算法来说，因为开奖号码由数据指纹唯一确定，数据指纹由彩票池原始数据唯一确定，所以开奖号码由原始数据唯一确定。

4、可信彩票系统的特点
4.1 随机性
开奖号码由所有被购买的彩票号码和一个已知的公开算法唯一确定，因为哈希算法的特点，结果具有不可预期的特点。原始数据的任何改变都会使最终的开奖号码全然不同——即使只改变其中的一位数字也是如此，由此可证任何一个彩票购买者的选择，都影响到了最终开奖号码。
4.2 可验证
任何人都可以下载到彩票池原始数据和开奖算法，并独立的对各个环节的计算进行验证。注意，最后一步的计算量十分庞大，普通PC难以在短时间内对全部数据段进行完整的验证，但可以选择其中任意的一段数据进行验证。

未完待续……
