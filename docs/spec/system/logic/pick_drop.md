# ピック・ドロップについて

ピック・ドロップや、その他の理由によって、ユーザーの所持パレットが増減する場合は、パレット総数の値を記録する必要がある。

## パレット総数の値の記録

これは、ユーザーが持っているパレットの種類を均等にするために必要な値である。

パレット総数は NoSQL に`パレットNo:パレット数`の形式で記録する。
パレット総数はあるユーザーが、パレットを獲得したら増える。ユーザー以外の処理では記録はされない。(スポットにパレットが落ちた場合などは関係ない)
**この処理は何があっても必ず行う。**

## スポットのパレットについて

スポットには複数のパレットが同時に落ちている可能性がある。

イベント開始時(スポット作成時)に一定数のパレットを初期配置として落としておく。
落とすパレットは、初期配置のパレット全体としておおよそ平均化されている必要がある。

スポットに落ちているパレットがゲーム性を全て決定付けるので、定期的にパレットの種類を平坦化する必要がある。
そのため定期的に、スポットに落ちているユーザーの取得率の高いパレットを低いパレットに変化させる処理を入れる必要がある可能性を考慮する。

## ドロップ

スポットに入った時に、自分が持っているパレットを落とし、スポットに落ちているパレットを拾うこと。
落とすと書くとパレットを失っているように思えるが、実際にはパレットの数は減らない。

### ドロップのロジック

パレットを持っている状態で、スポットに入った時に**完全にランダムで**パレットひとつを落とす。
パレットを持っている・いないに関わらず、スポットに入った時に**完全にランダムで**スポットに落ちているパレットをひとつ落とす。(拾ったパレットを既に持っていた場合は、スポットからは通常通り拾ったパレットがなくなり、参加者のパレットの数も増えない)

> 思想のメモ  
> ドロップの操作でシステム全体のパレットの収集率を安定化させるべきか否か  
> ...ユーザーが持っているパレットの確率が平坦化されているならば、完全ランダムでも良いのでは？  
> ただ、スポットにいるのに、パレットを拾わない=全然収集率が上がらない状況は避けたい  
> だれもパレットを拾わなくてパレットがスポットに残り続ける状況も避けたい  
> じゃあ、完全にランダムなドロップを行う&ドロップの回数を増やすことで、収集率を安定化させるのが良いのでは？

### ドロップの制限

ドロップは、全スポットで共通したユーザー固有のクールタイムが存在する。(これは、二つのスポットが同時に検知されている時に、どちらのスポットに入ってもドロップが発生しないようにするため。)

例えば、ユーザーはスポット A でドロップを行うと、ユーザー固有のクールタイムが明けるまで他のスポット(スポット B 等)に入ってもドロップは発生しない。
クールタイムが明けると、スポット に関わらず(たとえ、スポット A が連続しても)ドロップを行う。

## ピック

スポットで、QR コードを能動的にスキャンすることで、新たなパレットを獲得すること。

### ピックのロジック

スポットに入っている AND QR コードをスキャンした時に、パレットをひとつ獲得する。
獲得するパレットは、パレットの総数を使用し、パレットの種類をユーザー全体で均等になるように取得する。

### ピックの制限

ピックは、同じスポットでは連続して行えず、別のスポットでピックしたのちに、もう一度同じスポットでピックすることができる。
あるいは、一定時間経過後に同じスポットでピックすることができる。