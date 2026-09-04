Write-Host "`n===== 1. REGISTER USER =====" -ForegroundColor Cyan
$randomEmail = "test$(Get-Random)@gmail.com"
$registerBody = @{ name = "TestUser"; email = $randomEmail; password = "123456" } | ConvertTo-Json
try {
    $registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" -Method Post -ContentType "application/json" -Body $registerBody
    $registerResponse | ConvertTo-Json
}
catch {
    Write-Host "FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n===== 2. LOGIN =====" -ForegroundColor Cyan
$loginBody = @{ email = $randomEmail; password = "123456" } | ConvertTo-Json
$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
$loginResponse | ConvertTo-Json
$token = $loginResponse.token
$headers = @{ Authorization = "Bearer $token" }

Write-Host "`n===== 3. CREATE EVENT =====" -ForegroundColor Cyan
$eventBody = @{
    title       = "Tech Conference 2026"
    description = "Technology and AI conference"
    date        = "2026-10-15T10:00:00.000Z"
    location    = "Kanpur"
    capacity    = 100
} | ConvertTo-Json
$eventResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/events" -Method Post -ContentType "application/json" -Headers $headers -Body $eventBody
$eventResponse | ConvertTo-Json
$eventId = $eventResponse.data._id
Write-Host "Event ID: $eventId" -ForegroundColor Yellow

Write-Host "`n===== 4. GET ALL EVENTS =====" -ForegroundColor Cyan
$allEvents = Invoke-RestMethod -Uri "http://localhost:5000/api/events" -Method Get
Write-Host "Total events found: $($allEvents.count)"

Write-Host "`n===== 5. GET SINGLE EVENT =====" -ForegroundColor Cyan
$singleEvent = Invoke-RestMethod -Uri "http://localhost:5000/api/events/$eventId" -Method Get
$singleEvent | ConvertTo-Json

Write-Host "`n===== 6. UPDATE EVENT =====" -ForegroundColor Cyan
$updateBody = @{ location = "Delhi" } | ConvertTo-Json
$updateResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/events/$eventId" -Method Put -ContentType "application/json" -Headers $headers -Body $updateBody
$updateResponse | ConvertTo-Json

Write-Host "`n===== 7. REGISTER FOR EVENT =====" -ForegroundColor Cyan
$regResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/registrations/$eventId" -Method Post -Headers $headers
$regResponse | ConvertTo-Json

Write-Host "`n===== 8. DUPLICATE REGISTRATION CHECK (should FAIL) =====" -ForegroundColor Cyan
try {
    $dupResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/registrations/$eventId" -Method Post -Headers $headers
    Write-Host "UNEXPECTED SUCCESS - duplicate prevention NOT working!" -ForegroundColor Red
}
catch {
    $errorBody = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "Correctly blocked: $($errorBody.message)" -ForegroundColor Green
}

Write-Host "`n===== 9. MY REGISTERED EVENTS =====" -ForegroundColor Cyan
$myEvents = Invoke-RestMethod -Uri "http://localhost:5000/api/registrations/my-events" -Method Get -Headers $headers
$myEvents | ConvertTo-Json

Write-Host "`n===== 10. CANCEL REGISTRATION =====" -ForegroundColor Cyan
$cancelResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/registrations/$eventId" -Method Delete -Headers $headers
$cancelResponse | ConvertTo-Json

Write-Host "`n===== 11. DELETE EVENT =====" -ForegroundColor Cyan
$deleteResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/events/$eventId" -Method Delete -Headers $headers
$deleteResponse | ConvertTo-Json

Write-Host "`n===== ALL TESTS COMPLETE =====" -ForegroundColor Green