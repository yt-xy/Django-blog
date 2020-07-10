### queryset
queryset本质上是一个懒加载，代码执行后不会进行数据库查询操作，只是会返回一个queryset对象，等你真正使用时才会执行查询
```python
posts = post.objects.all()  # 返回一个questset对象并赋值给posts
available_posts = posts.filter(status=1)  # 继续返回一个queryset对象并赋值给available_posts
print(available_posts)  # 此时会根据上面的两个条件执行数据查询操作
# 对应的sql语句为：select * from blog_post where status=1;
```

链式调用：执行一个对象中的方法之后得到的结果还是这个对象，这样就可以直接执行对象上的其他方法，因为每个函数的返回值都是它自己(queryset)

#### 常用的queryset接口
1. 支持链式调用的接口 => 返回值是QuerySet的接口
-all接口：相当于`SELECT * FROM table_name`
-filter接口：根据条件过滤数据，常用的条件基本上是字段等于、不等于、大于、小于，以及类似LIKE查询的`Model.objects.filter(content__contains='条件`
-exclude接口：同filter，只是相反的逻辑
-reverse接口：把QuerySet中的结果倒序排序
-distinct接口：用来进行去重查询，产生`SELECT DISTINCT`这样的查询
-none接口：返回空的QuestSet
<hr />

2. 不接受链式调用的接口 => 返回值不是QuerySet的接口
-get接口：如果存在，则直接返回对应的Post示例；如果不存在，则抛出DoesNotExist异常
-create接口：用来创建一个Model对象
-get_or_create接口：根据条件查找，如果没查找到，就调用create创建
-count接口：用于返回QuestSet有多少条记录，相当于`SELECT COUNT(*) FROM table_name`
-latest接口：用于返回最新的一条记录，但是需要在Model的Meta中定义：get_latest_by = <用来排序的字段>
-earliest接口：同上，返回最早的一条记录
-first接口：从当前QuerySet记录中获取第一条
-last接口：同上，获取最后一条
-exists接口：返回True或False，在数据库层面执行`SELECT (1) AS 'a' FROM table_name LIMIT 1`的查询，如果只是需要判断QuerySet是否有数据，用这个接口是最合适的方式。
            不要用count或者len(queryset)这样的操作来判断数据是否存在。相反，如果可以预期接下来会用到QuerySet中的数据，可以考虑使用len(queryset)的方式来做判断，这样可以减少一次DB操作
-bulk_create接口：同create，用来批量创建记录
-in_bulk接口：批量查询，接收两个参数 id_list 和 filed_name。`Post.objects.inbulk([1,2,3])`
-update接口：用来根据条件批量更新记录。`Post.objects.filter(owner__name='yt').update(title='测试更新')`
-delete接口：同update，这个接口是用来根据条件批量删除记录
-values接口：当我们明确知道只需要返回某个字段的值，不需要Model实例时，可以使用
-values_list接口：同values，但是直接返回的是包含tuple的QuerySet。如果只是一个字段的话，可以通过增加flat=True参数，便于我们后续处理
<hr />

3. 进阶接口
-defer接口：把不需要展示的字段做延迟加载。比如说，需要获取到文章中除正文外的其他字段`posts=Post.objects.all().defer('content')` [注意：可能会产生N+1查询问题]
-only接口：同defer相反，如果只想获取到所有的title记录，就可以使用only，只获取title的内容，其他值在获取时会产生额外的查询
-select_related接口：用于解决外键产生的N+1问题
```python
posts = Post.objects.all()
for post in posts: # 产生数据库查询
    print(post.owner) # 产生额外的数据库查询
    
posts = Post.objects.all().select_related('category')
for post in posts: # 产生数据库查询，category数据也会一次性查询出来
    print(post.category)
```
-prefetch_related接口：用来避免多对多关系产生的N+1问题
```python
posts = Post.objects.all().prefetch_related('tag')
for post in posts:
    print(post.tag.all())
```
<hr />

4. 常用的字段查询
-contains：包含，用来进行相似查询
-icontains：同contains，只是忽略大小写
-exact：精确匹配
-iexact：同iexact，只是忽略大小写
-in：指定某个集合。`Post.objects.filter(id__in=[1,2,3]`=>`SELECT * FROM blog_post WHERE IN (1,2,3)`
-gt：大于某个值
-gte：大于等于某个值
-lt：小于某个值
-lte：小于等于某个值
-startswitch：以某个字符串开头，与contains类似，只是会产生`LIKE '<关键词>%’`这样的SQL
-istartswitch：同startswitch，忽略大小写
-endswitch：以某个字符串结尾
-iendswitch：同endswitch，忽略大小写
-range：范围查询，多用于时间范围
<hr />

5. 进阶查询
-F：F表达式常用来执行数据库层面的计算，从而避免出现竞争状态。
```python
# 比如需要处理每篇文章的访问量，假设存在post.pv这样的字段，当有用户访问时，我们对其加1
post = Post.objects.get(id=1)
post.pv = post.pv + 1
pos.save()
# 在多线程的情况下会出现问题，其执行逻辑是先获取到当前的pv值，然后将其加1后赋值给post.pv，最后保存
# 如果多个线程同时执行，那么每个线程里的post.pv值都是一样的，执行完加1保存后，相当于只执行了一个加1，而不是多个
# 原因在于我们把数据拿到Python中转了一圈，然后再保存到数据库中。
from django.db.models import F
post = Post.objects.get(id=1)
post.pv = F('pv') + 1
post.save()
```
<hr />

-Q：Q表达式用于解决OR，AND查询
```python
from django.db.models import Q
Post.objects.filter(Q(id=1) | Q(id=2)) # OR
post.objects.filter(Q(id=1) & Q(id=2)) # AND
```
<hr />

-Count：用来做聚合查询
```python
# 比如想要得到某个分类下有多少篇文章
category = Category.objects.get(id=1)
posts_count = category.post_set.count()
# 但是如果想要把这个结果放到category上
from django.db.models import Count
categories = Category.objects.annotate(posts_count=Count('post'))
print(categories[0].posts_count)
```
<hr />

-Sum：同Count类似，用来做合计
```python
# 比如统计目前所有文章加起来的访问量
from django.db.models import Sum
Post.objects.aggregate(all_pv=Sum('pv)) # 输出类似结果：{'all_pv': 487}
```