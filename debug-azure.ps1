$Body = @{“region”=“all”;“request”=“dcip”} | ConvertTo-Json

$WebRequest= Invoke-WebRequest -Method “POST” -uri `https://azuredcip.azurewebsites.net/api/azuredcipranges -Body $Body

ConvertFrom-Json -InputObject $WebRequest.Content
