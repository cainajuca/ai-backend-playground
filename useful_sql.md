## SKUs' relevant info
```sql
select
	s.Id,
	b.Name,
	s.SizeValue, 
	u.Symbol,
	p.Description,
	t.Name ProductType
from Skus s
	join Brands b on b.id = s.BrandId
	join units u on u.id = s.unitid
	join Products p on p.id = s.ProductId
	join ProductTypes t on t.id = p.TypeId
```

## Carts' relevant info
```sql
select 
    ci.Quantity, 
    s.SizeValue, 
    b.Name,
    u.Name, u.Symbol,
    p.Description,
    t.Name ProductType
from cartitems ci
    join Skus s on s.id = ci.SkuId
    join Brands b on b.id = s.BrandId
    join units u on u.id = s.unitid
    join Products p on p.id = s.ProductId
    join ProductTypes t on t.id = p.TypeId
```

